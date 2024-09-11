#!/usr/bin/python3
#from bottle import route, run, template
from bottle import template, request, post, route
from datetime import datetime

@route('/start', method='POST')
def start():
    post_data=request.body.read()
    return template("initial_page.html",post_data=post_data)

@route('/world')
def hello():
    return "Hello India World!"
    
@route('/')
def index():
    ddd=datetime.today().strftime('%Y-%m-%d %M:%S')	
    return template("index.html",variable=ddd)
