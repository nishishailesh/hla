#!/usr/bin/python3
#from bottle import route, run, template
from bottle import template, request, post, route, redirect
from datetime import datetime

basepath="hla"

@route('/')
def index():
    ddd=datetime.today().strftime('%Y-%m-%d %M:%S') 
    return template("index.html",variable=ddd,basepath=basepath)



@route('/start', method='POST')
def start():
    post_data=request.body.read()
    if(request.forms.get("uname")=="shailesh" and request.forms.get("psw")=="shailesh"):
      return template("initial_page.html",post_data=post_data)
    else:
      return template("failed_login.html",post_data=post_data)


    
