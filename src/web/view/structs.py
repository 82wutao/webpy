
from bottle import view



@view("index.tpl")
def index():
    a = dict()
    a["d"] = ""
    return a
