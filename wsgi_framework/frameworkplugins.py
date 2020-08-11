###############################################################################
# Plugins ######################################################################
###############################################################################
import sys

from wsgi_framework import exceptions
from wsgi_framework import settings
from wsgi_framework import http_wsgi
from wsgi_framework import template_adapters

class PluginError(exceptions.BottleException): pass


class JSONPlugin(object):
    name = 'json'
    api  = 2

    def __init__(self, json_dumps=settings.json_dumps):
        self.json_dumps = json_dumps

    def apply(self, callback, route):
        dumps = self.json_dumps
        if not dumps: return callback
        def wrapper(*a, **ka):
            try:
                rv = callback(*a, **ka)
            except http_wsgi.HTTPError:
                rv = settings._e()

            if isinstance(rv, dict):
                #Attempt to serialize, raises exception on failure
                json_response = dumps(rv)
                #Set content type only if serialization succesful
                http_wsgi.response.content_type = 'application/json'
                return json_response
            elif isinstance(rv, http_wsgi.HTTPResponse) and isinstance(rv.body, dict):
                rv.body = dumps(rv.body)
                rv.content_type = 'application/json'
            return rv

        return wrapper


class TemplatePlugin(object):
    ''' This plugin applies the :func:`view` decorator to all routes with a
        `template` config parameter. If the parameter is a tuple, the second
        element must be a dict with additional options (e.g. `template_engine`)
        or default variables for the template. '''
    name = 'template'
    api  = 2

    def apply(self, callback, route):
        conf = route.config.get('template')
        if isinstance(conf, (tuple, list)) and len(conf) == 2:
            return template_adapters.view(conf[0], **conf[1])(callback)
        elif isinstance(conf, str):
            return template_adapters.view(conf)(callback)
        else:
            return callback


#: Not a plugin, but part of the plugin API. TODO: Find a better place.
class _ImportRedirect(object):
    def __init__(self, name, impmask):
        ''' Create a virtual package that redirects imports (see PEP 302). '''
        self.name = name
        self.impmask = impmask
        self.module = sys.modules.setdefault(name, settings.new_module(name))
        self.module.__dict__.update({'__file__': __file__, '__path__': [],
                                    '__all__': [], '__loader__': self})
        sys.meta_path.append(self)

    def find_module(self, fullname, path=None):
        if '.' not in fullname: return
        packname = fullname.rsplit('.', 1)[0]
        if packname != self.name: return
        return self

    def load_module(self, fullname):
        if fullname in sys.modules: return sys.modules[fullname]
        modname = fullname.rsplit('.', 1)[1]
        realname = self.impmask % modname
        __import__(realname)
        module = sys.modules[fullname] = sys.modules[realname]
        setattr(self.module, modname, module)
        module.__loader__ = self
        return module



#: A virtual package that redirects import statements.
#: Example: ``import bottle.ext.sqlite`` actually imports `bottle_sqlite`.
ext = _ImportRedirect('bottle.ext' if __name__ == '__main__' else __name__+".ext", 'bottle_%s').module