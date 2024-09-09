#!/usr/bin/python3
from bottle import route, run, template
from datetime import datetime

@route('/hello')
def hello():
    return "Hello World!"

@route('/world')
def hello():
    return "Hello India World!"
    
@route('/')
def hello():
    ddd=datetime.today().strftime('%Y-%m-%d %M:%S')	
    return template("index.html",variable=ddd)
