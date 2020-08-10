import bottle









# def application(environ, start_response):
#     for k,v in environ.items():
#         print("in env K %s ,v %s\n"% (k,v))
#     start_response('200 OK', [('Content-Type', 'text/html')])
#     return "<h1>Hello, web!</h1>".encode('utf8')
#
#
# from mywsgiref.simple_server import make_server
# httpd = make_server('', 8000, application)
# print("Serving HTTP on port 8000...")
#
# httpd.serve_forever()
