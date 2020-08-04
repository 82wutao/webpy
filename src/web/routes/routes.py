

from web.view import structs

def load_routes(bottle_app,ctx_root):
    bottle_app.route('%s' % ctx_root, ['GET', 'POST'], structs.index)
    bottle_app.route('%s/index.html' % ctx_root, ['GET', 'POST'], structs.index)

    # bottle_app.route('/edit', ['GET', 'POST'], form_edit)