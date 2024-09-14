#!/usr/bin/python3
#from bottle import route, run, template
from bottle import template, request, post, route, redirect
from datetime import datetime
from mysql_lis import mysql_lis
import sys, logging, bcrypt
#For mysql password
sys.path.append('/var/gmcs_config')
###########Setup this for getting database,user,pass for HLA database##########
import astm_var_hla as astm_var
##############################################################
logging.basicConfig(filename="/var/log/hla.log",level=logging.DEBUG)  

@route('/start', method='POST')
def start():
    post_data=request.body.read()
    if(verify_user()==True):
      return template("initial_page.html",post_data=post_data)
    else:
      return template("failed_login.html",post_data=post_data)
    
@route('/')
def index():
    return template("index.html")

@route('/view_antigen', method='POST')
def view_antigen():
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
  cur=m.run_query(con,prepared_sql='select * from antigen',data_tpl=())
  all_data=m.get_all_rows(cur)
  if(all_data==None):
    logging.debug('antigen data not found')
    return False
  m.close_cursor(cur)
  m.close_link(con)  
  return template("view_antigen.html",all_data=all_data)
    
def verify_user():
  if(request.forms.get("uname")!=None and request.forms.get("psw")!=None):
    uname=request.forms.get("uname")
    psw=request.forms.get("psw")
    logging.debug('username and password are provided')
    m=mysql_lis()
    con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
    cur=m.run_query(con,prepared_sql='select * from user where user=%s',data_tpl=(uname,))
    user_info=m.get_single_row(cur)
    if(user_info==None):
      logging.debug('user {} not found'.format(uname))
      return False
    m.close_cursor(cur)
    m.close_link(con)

    '''
    Python: bcrypt.hashpw(b'mypassword',bcrypt.gensalt(rounds= 4,prefix = b'2b')
    PHP:    password_hash('mypassword',PASSWORD_BCRYPT);

    Python:bcrypt.checkpw(b'text',b'bcrypted password')
    PHP: password_verify('text,'bcrypted password')
    '''
    #try is required to cache NoneType exception when supplied hash is not bcrypt
    try:
      if(bcrypt.checkpw(psw.encode("UTF-8"),user_info[2].encode("UTF-8"))==True):
        return True
      else:
        return False
    except Exception as ex:
      logging.debug('{}'.format(ex))
      return False
