from bottle import route, run, template






@route('/hello/*')
def log_filter():
    print("loging")
    pass


@route('/hello/world')
def index(name="abc"):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)




# hello.py

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'

# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from hello import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print "Serving HTTP on port 8000..."
# 开始监听HTTP请求:
httpd.serve_forever()


# http server ======>                  uWSGI{托管了usgi的规范的应用}
#   nginx    {socket ,http ,uwsgi}