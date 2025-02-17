#!/usr/bin/python3
#from bottle import route, run, template
from bottle import template, request, post, route, redirect
from datetime import datetime
from mysql_lis import mysql_lis
import sys, logging, bcrypt, csv, pprint
from functools import wraps
from io import StringIO

#For mysql password
sys.path.append('/var/gmcs_config')
###########Setup this for getting database,user,pass for HLA database##########
import astm_var_hla as astm_var
##############################################################
logging.basicConfig(filename="/var/log/hla.log",level=logging.DEBUG)  

collection_string=''    
#this goes on increasing at each run. 
#wsgi create functions and use. 
#so it is not reset everytime page 
#reset when there is pache restart
#so zero out it at each route function
 
def log_and_display(log_data,display=0):
  global collection_string
  logging.debug(log_data)
  if(display!=0):
    collection_string=collection_string+'<hr><pre>{}</pre>'.format(log_data)
    
def tuple_to_html(tpl):
  str(tpl).replace(',','<li>').replace('(','<ul>').replace(')','</ul>').replace('{','<ul>').replace('}','</ul>')
  return tpl
  
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
      m.close_cursor(cur)
      m.close_link(con)
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
        logging.debug('user {}: password verification successful'.format(uname))
        return True
      else:
        return False
    except Exception as ex:
      logging.debug('{}'.format(ex))
      return False
  else:
    logging.debug("else reached")
    return False
    
def decorate_verify_user(fun):
  def nothing():
    logging.debug("no username password available") 
    return template("failed_login.html",post_data="No post_data")
  @wraps(fun)   #not essential
  def do_it():
    if(verify_user()==True):
      logging.debug("#fun() reached...")
      return fun()  #return essential to return template
    else:
      return nothing() #return essential to return template
  logging.debug("function name of do_it is {}".format(do_it.__name__))
  return do_it
    
@route('/start', method='POST')
def start():
    post_data=request.body.read()
    uname=request.forms.get("uname")
    psw=request.forms.get("psw")
    if(verify_user()==True):
      return template("initial_page.html",post_data=post_data,uname=uname,psw=psw)
    else:
      return template("failed_login.html",post_data=post_data,uname=uname,psw=psw)
    
@route('/')
def index():
    return template("index.html")

@route('/view_antigen', method='POST')
@decorate_verify_user
def view_antigen():
  logging.debug('view_antigen() entered...')
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
  cur=m.run_query(con,prepared_sql='select * from antigen',data_tpl=())
  all_data=m.get_all_rows(cur)
  logging.debug("antigen data:{}".format(all_data))
  if(all_data==None):
    logging.debug('antigen data not found')
    m.close_cursor(cur)
    m.close_link(con)
    return False
  m.close_cursor(cur)
  m.close_link(con)  
  logging.debug('view_antigen.html entering...')
  return template("view_antigen.html",all_data=all_data)

@route('/get_SAB_plate_csv', method='POST')
@decorate_verify_user
def get_SAB_plate_csv():
  return template("get_SAB_plate_csv.html")



'''
class FileUpload[source]
    file        Open file(-like) object (BytesIO buffer or temporary file)
    name        Name of the upload form field
    raw_filename        Raw filename as sent by the client (may contain unsafe characters)
    headers        A HeaderDict with additional headers (e.g. content-type)
    content_type        Current value of the ‘Content-Type’ header.
    content_length        Current value of the ‘Content-Length’ header.
    get_header(name, default=None)[source]        Return the value of a header within the multipart part.
    filename()[source]        Name of the file on the client file system, but normalized to ensure file system compatibility. An empty filename is returned as ‘empty’.
    save(destination, overwrite=False, chunk_size=65536)    Save file to disk or copy its content to an open file(-like) object. If destination is a directory, filename is added to the path. Existing files are not overwritten by default (IOError).
        Parameters:                destination – File path, directory or file(-like) object.                overwrite – If True, replace existing files. (default: False)
                chunk_size – Bytes to read at a time. (default: 64kb)
'''



'''
@route('/save_class_one_import', method='POST')
@decorate_verify_user
def do_upload_class_1():
  global collection_string
  collection_string=''
  from import_report_csv_1 import save_report_csv_1_io
  all_file_objects= request.files
  log_and_display("all_file_objects keys:{}".format(all_file_objects.keys()))       #Class Files
  log_and_display("total file objects in this form:{}".format(len(all_file_objects)))
  for one_file_object in list(all_file_objects.keys()):                           #Class fileUpload
    log_and_display("one file object key:{}".format(one_file_object),1)
    log_and_display("one file object file io object:{}".format(all_file_objects[one_file_object].file),1)
    log_and_display("one file object name of form upload field:{}".format(all_file_objects[one_file_object].name))
    log_and_display("one file object raw_filename (original with spaces etc):{}".format(all_file_objects[one_file_object].raw_filename))    
    log_and_display("one file object headers (dict ype):{}".format(all_file_objects[one_file_object].headers))    
    log_and_display("one file object headers data:{}".format(dict(all_file_objects[one_file_object].headers)))    
    log_and_display("one file object content_type:{}".format(all_file_objects[one_file_object].content_type))    
    log_and_display("one file object content_length:{}".format(all_file_objects[one_file_object].content_length))    
    log_and_display("one file object space etc removed filename:{}".format(all_file_objects[one_file_object].filename) )   
    
    #log_and_display("=====file data======")
    #log_and_display("one file object file io object read() (like any other io handle):{}".format(all_file_objects[one_file_object].file.read()))
    patient_id=save_report_csv_1_io(all_file_objects[one_file_object].file)
  #return template("dummy.html",files=collection_string)
  html_data=view_recipient_detail_new_class_1(patient_id)
  return template("view_recipient_detail.html",html_data)
'''
@route('/save_class_two_import_old', method='POST')
@decorate_verify_user
def do_upload_class_2():
  global collection_string
  collection_string=''
  from import_report_csv_2 import save_report_csv_2_io
  all_file_objects= request.files
  log_and_display("all_file_objects keys:{}".format(all_file_objects.keys()))       #Class Files
  log_and_display("total file objects in this form:{}".format(len(all_file_objects)))
  for one_file_object in list(all_file_objects.keys()):                           #Class fileUpload
    log_and_display("one file object key:{}".format(one_file_object),1)
    log_and_display("one file object file io object:{}".format(all_file_objects[one_file_object].file))
    log_and_display("one file object name of form upload field:{}".format(all_file_objects[one_file_object].name))
    log_and_display("one file object raw_filename (original with spaces etc):{}".format(all_file_objects[one_file_object].raw_filename))    
    log_and_display("one file object headers (dict ype):{}".format(all_file_objects[one_file_object].headers))    
    log_and_display("one file object headers data:{}".format(dict(all_file_objects[one_file_object].headers)))    
    log_and_display("one file object content_type:{}".format(all_file_objects[one_file_object].content_type))    
    log_and_display("one file object content_length:{}".format(all_file_objects[one_file_object].content_length))    
    log_and_display("one file object space etc removed filename:{}".format(all_file_objects[one_file_object].filename) )   
    
    #log_and_display("=====file data======")
    #log_and_display("one file object file io object read() (like any other io handle):{}".format(all_file_objects[one_file_object].file.read()))
    patient_id=save_report_csv_2_io(all_file_objects[one_file_object].file)
  #return template("dummy.html",files=collection_string)
  html_data=view_recipient_detail_new_class_2(patient_id)
  return template("view_recipient_detail.html",html_data)


@route('/save_class_two_import', method='POST')
@decorate_verify_user
def do_upload_class_2():
  global collection_string
  collection_string=''
  from import_report_csv_2 import save_report_csv_2_io
  all_file_objects= request.files
  log_and_display("all_file_objects keys:{}".format(all_file_objects.keys()))       #Class Files
  log_and_display("total file objects in this form:{}".format(len(all_file_objects)))
  for one_file_object in list(all_file_objects.keys()):                           #Class fileUpload
    log_and_display("one file object key:{}".format(one_file_object),1)
    log_and_display("one file object file io object:{}".format(all_file_objects[one_file_object].file))
    log_and_display("one file object name of form upload field:{}".format(all_file_objects[one_file_object].name))
    log_and_display("one file object raw_filename (original with spaces etc):{}".format(all_file_objects[one_file_object].raw_filename))    
    log_and_display("one file object headers (dict ype):{}".format(all_file_objects[one_file_object].headers))    
    log_and_display("one file object headers data:{}".format(dict(all_file_objects[one_file_object].headers)))    
    log_and_display("one file object content_type:{}".format(all_file_objects[one_file_object].content_type))    
    log_and_display("one file object content_length:{}".format(all_file_objects[one_file_object].content_length))    
    log_and_display("one file object space etc removed filename:{}".format(all_file_objects[one_file_object].filename) )   
    
    #log_and_display("=====file data======")
    #log_and_display("one file object file io object read() (like any other io handle):{}".format(all_file_objects[one_file_object].file.read()))
  
  patient_id =save_report_csv_2_io(all_file_objects[one_file_object].file)
  #html_data=view_recipient_detail_new_class_1(patient_id)
  #return template("view_recipient_detail.html",html_data=[patient_id,collection_string])
  return template("dummy.html",html_data={'patient_id':patient_id,'collection_string':collection_string})





@route('/save_class_one_import', method='POST')
@decorate_verify_user
def do_upload_class_1():
  global collection_string
  collection_string=''
  from import_report_csv_1 import save_report_csv_1_io
  all_file_objects= request.files
  log_and_display("all_file_objects keys:{}".format(all_file_objects.keys()))       #Class Files
  log_and_display("total file objects in this form:{}".format(len(all_file_objects)))
  for one_file_object in list(all_file_objects.keys()):                           #Class fileUpload
    log_and_display("one file object key:{}".format(one_file_object),1)
    log_and_display("one file object file io object:{}".format(all_file_objects[one_file_object].file))
    log_and_display("one file object name of form upload field:{}".format(all_file_objects[one_file_object].name))
    log_and_display("one file object raw_filename (original with spaces etc):{}".format(all_file_objects[one_file_object].raw_filename))    
    log_and_display("one file object headers (dict ype):{}".format(all_file_objects[one_file_object].headers))    
    log_and_display("one file object headers data:{}".format(dict(all_file_objects[one_file_object].headers)))    
    log_and_display("one file object content_type:{}".format(all_file_objects[one_file_object].content_type))    
    log_and_display("one file object content_length:{}".format(all_file_objects[one_file_object].content_length))    
    log_and_display("one file object space etc removed filename:{}".format(all_file_objects[one_file_object].filename) )   
    
    #log_and_display("=====file data======")
    #log_and_display("one file object file io object read() (like any other io handle):{}".format(all_file_objects[one_file_object].file.read()))
  
  patient_id =save_report_csv_1_io(all_file_objects[one_file_object].file)
  #html_data=view_recipient_detail_new_class_1(patient_id)
  #return template("view_recipient_detail.html",html_data=[patient_id,collection_string])
  return template("dummy.html",html_data={'patient_id':patient_id,'collection_string':collection_string})



@route('/import_SAB_plate_csv', method='POST')
@decorate_verify_user
def do_upload():
  upload= request.files.get('SAB_csv')    #gets files object (like forms object -> post data)
  line_data=upload.file.read()
  rd = csv.reader(StringIO(line_data.decode("UTF-8")), delimiter=',')
  msg=()
  median=[]
  next_message=''
  all_data=[]
  for i in rd:
    all_data=all_data+[i]
    if(len(i)>=2):
      if(i[0]=='DataType:' and i[1]=='Median'):
        msg=msg+("Median data will be analysed",)
        next_message='Median'
        continue
    if(next_message=='Median'):
      if(len(i)==0):
        next_message=''
      median=median+[i]
      
  analyse_file_data(all_data)
  return template("import_SAB_plate_csv.html",file_data=all_data,msg=msg,median=median)





@route('/get_donor_detail', method='POST')
@decorate_verify_user
def get_patient_detail():
    uname=request.forms.get("uname")
    psw=request.forms.get("psw")
    return template("get_donor_detail.html",uname=uname,psw=psw)



@route('/get_recipient_detail', method='POST')
@decorate_verify_user
def get_patient_detail():
    uname=request.forms.get("uname")
    psw=request.forms.get("psw")
    return template("get_recipient_detail.html",uname=uname,psw=psw)



@route('/view_donor_detail', method='POST')
@decorate_verify_user
def view_donor_detail():
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  patient_id=request.forms.get("patient_id")  
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
  patient_id=request.forms.get("patient_id")
  sql='select * from donor where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_data=m.get_single_row(cur)
  logging.debug("patient_data:{}".format(patient_data))


  if(patient_data==None):
    logging.debug("No donor data found for such donor id")
  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  
  if(patient_data==None):
    data_dict=None
  else:
    data_dict=dict(zip(field_names,patient_data))
    
  logging.debug("data_dict:{}".format(data_dict))
  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict,
  'uname':uname,
  'psw':psw
  }
  print(data_dict)
  return template("view_donor_detail.html",html_data)
  
  

@route('/edit_donor_detail', method='POST')
@decorate_verify_user
def edit_donor_detail():
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  patient_id=request.forms.get("patient_id")
    
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)

  sql='select * from donor where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_data=m.get_single_row(cur)
  logging.debug("patient_data:{}".format(patient_data))


  if(patient_data==None):
    logging.debug("No donor data found for such donor id")
  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  
  if(patient_data==None):
    data_dict=None
  else:
    data_dict=dict(zip(field_names,patient_data))
    
  logging.debug("data_dict:{}".format(data_dict))
  m.close_link(con)
  html_data={
  'uname':uname,
  'psw':psw,
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict
  }
  print(data_dict)
  return template("edit_donor_detail.html",html_data)
  

@route('/delete_donor_detail', method='POST')
@decorate_verify_user
def delete_donor_detail():
  global collection_string
  collection_string=''
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
  patient_id=request.forms.get("patient_id")
  sql='delete from donor where patient_id=%s'
  log_and_display("sql:{}".format(sql))
  data_tpl=(patient_id,)
  log_and_display("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  log_and_display("last_message{}".format(m.last_message),1)
  
  patient_data=m.get_single_row(cur)
  log_and_display("patient_data:{}".format(patient_data))
  if(patient_data==None):
    log_and_display("<p class='text-danger'>No donor data found for such recipient id:{}, so, successfully deleted. recipient antibody data may persist</p>".format(patient_id),1)

  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'collection_string':collection_string
  }
  return template("delete_donor_detail.html",html_data=html_data)
  
######Recipient edit delete########

@route('/edit_recipient_detail', method='POST')
@decorate_verify_user
def edit_recipient_detail():
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  patient_id=request.forms.get("patient_id")
    
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)

  sql='select * from recipient where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_data=m.get_single_row(cur)
  logging.debug("patient_data:{}".format(patient_data))


  if(patient_data==None):
    logging.debug("No recipient data found for such donor id")
  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  
  if(patient_data==None):
    data_dict=None
  else:
    data_dict=dict(zip(field_names,patient_data))
    
  logging.debug("data_dict:{}".format(data_dict))
  m.close_link(con)
  html_data={
  'uname':uname,
  'psw':psw,
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict
  }
  print(data_dict)
  return template("edit_recipient_detail.html",html_data)




  

@route('/delete_recipient_detail', method='POST')
@decorate_verify_user
def delete_recipient_detail():
  global collection_string
  collection_string=''
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
  patient_id=request.forms.get("patient_id")
  sql='delete from recipient where patient_id=%s'
  log_and_display("sql:{}".format(sql))
  data_tpl=(patient_id,)
  log_and_display("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  log_and_display("last_message{}".format(m.last_message),1)
  
  patient_data=m.get_single_row(cur)
  log_and_display("patient_data:{}".format(patient_data))
  if(patient_data==None):
    log_and_display("<p class='text-danger'>No recipient data found for such recipient id:{}, so, successfully deleted. recipient antibody data may persist</p>".format(patient_id),1)

  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'collection_string':collection_string
  }
  return template("delete_recipient_detail.html",html_data=html_data)
  
############End of Recipient edit delete section ###############  
@route('/view_recipient_detail', method='POST')
@decorate_verify_user
def view_recipient_detail():
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
  patient_id=request.forms.get("patient_id")

  #############HLA Details#############
  sql='select * from recipient where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_data=m.get_single_row(cur)
  logging.debug("patient_data:{}".format(patient_data))


  if(patient_data==None):
    logging.debug("No recipient data found for such patient id")
    
  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  if(patient_data==None):
    data_dict=None
  else:
    data_dict=dict(zip(field_names,patient_data))
  logging.debug("data_dict:{}".format(data_dict))
  m.close_cursor(cur)
  
  #############HLA single antigen Details#############
  sql='select * from recipient_antibodies where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_antibodies_data=m.get_all_rows(cur)
  logging.debug("patient_antibodies_data:{}".format(patient_data))


  if(patient_antibodies_data==None):
    logging.debug("No recipient_antibodies data found for such patient id")
  m.close_cursor(cur)
  
  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict,
  'patient_antibodies_data':patient_antibodies_data,
  'uname':uname,
  'psw':psw
  }
  return template("view_recipient_detail.html",html_data)
  


#for class I rsult display after import
def view_recipient_detail_new_class_1(patient_id):
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)

  #############HLA Details#############
  sql='select * from recipient where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_data=m.get_single_row(cur)
  logging.debug("patient_data:{}".format(patient_data))


  if(patient_data==None):
    logging.debug("No recipient data found for such patient id")
    
  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  if(patient_data==None):
    data_dict=None
  else:
    data_dict=dict(zip(field_names,patient_data))
  logging.debug("data_dict:{}".format(data_dict))
  m.close_cursor(cur)
  
  #############HLA single antigen Details#############
  sql='select * from single_antigen_1_csv_report  where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_antibodies_data=m.get_all_rows(cur)
  logging.debug("patient_antibodies_data [ CLASS I ] :{}".format(patient_antibodies_data))


  if(patient_antibodies_data==None):
    logging.debug("No recipient_antibodies [ CLASS I ] data found for such patient id")
  m.close_cursor(cur)
  
  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict,
  'patient_antibodies_data':patient_antibodies_data,
  'uname':uname,
  'psw':psw
  }
  #return template("view_recipient_detail.html",html_data)
  return html_data
  
#for class I rsult display after import
def view_recipient_detail_new_class_2(patient_id):
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)

  #############HLA Details#############
  sql='select * from recipient where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_data=m.get_single_row(cur)
  logging.debug("patient_data:{}".format(patient_data))


  if(patient_data==None):
    logging.debug("No recipient data found for such patient id")
    
  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  if(patient_data==None):
    data_dict=None
  else:
    data_dict=dict(zip(field_names,patient_data))
  logging.debug("data_dict:{}".format(data_dict))
  m.close_cursor(cur)
  
  #############HLA single antigen Details#############
  sql='select * from single_antigen_2_csv_report  where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_antibodies_data=m.get_all_rows(cur)
  logging.debug("patient_antibodies_data [ CLASS II ] :{}".format(patient_antibodies_data))


  if(patient_antibodies_data==None):
    logging.debug("No recipient_antibodies [ CLASS II ] data found for such patient id")
  m.close_cursor(cur)
  
  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict,
  'patient_antibodies_data':patient_antibodies_data,
  'uname':uname,
  'psw':psw
  }
  #return template("view_recipient_detail.html",html_data)
  return html_data
  


@route('/save_new_donor', method='POST')
@decorate_verify_user
def save_new_donor():
  post_dict=dict(request.forms.items())
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  pid=request.forms.get("patient_id")
  
  logging.debug(post_dict)
  post_dict.pop("action")
  post_dict.pop("uname")
  post_dict.pop("psw")
  logging.debug(post_dict)
  
  #{'patient_id': '1234', 'name': 'ok kjj', 'ABO': 'A', 'Rh': 'Positive', 'HLA-A_allele-1': '', 'HLA-A_allele-2': '', 'HLA-B_allele-1': '', 'HLA-B_allele-2': '', 'HLA-Bw_allele-1': '', 'HLA-Bw_allele-2': '', 'HLA-Cw_allele-1': '', 'HLA-Cw_allele-2': '', 'HLA-DRB1_allele-1': '', 'HLA-DRB1_allele-2': '', 'HLA-DRB3_allele-1': '', 'HLA-DRB3_allele-2': '', 'HLA-DRB4_allele-1': '', 'HLA-DRB4_allele-2': '', 'HLA-DRB5_allele-1': '', 'HLA-DRB5_allele-2': '', 'HLA-DQA1_allele-1': '', 'HLA-DQA1_allele-2': '', 'HLA-DQB1_allele-1': '', 'HLA-DQB1_allele-2': '', 'action': '/hla/save_new_patient'} 
  keys_section='`'+'`,`'.join(post_dict.keys())+'`'
  values_section='"'+'","'.join(post_dict.values())+'"'
  sql='insert into  donor ('+keys_section+') values ('+values_section+')'
  logging.debug("insert sql:{}".format(sql))
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  cur=m.run_query(con,prepared_sql=sql,data_tpl=())
  m.close_link(con)
  return template("save_new_donor.html",post_dict=post_dict,last_message=m.last_message,psw=psw,pid=pid,uname=uname,patient_id=pid)  

@route('/save_edited_donor', method='POST')
@decorate_verify_user
def save_edited_donor():
  global collection_string
  collection_string=''
  post_dict=dict(request.forms.items())
  
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  pid=request.forms.get("patient_id")
   
  log_and_display('post data before removing unncessary post values:{}'.format(post_dict),1)
  post_dict.pop("action")
  post_dict.pop("uname")
  post_dict.pop("psw")
  post_dict.pop("patient_id")


  log_and_display('post data AFTER removing unncessary post values:{}'.format(post_dict),1)
  #{'patient_id': '1234', 'name': 'ok kjj', 'ABO': 'A', 'Rh': 'Positive', 'HLA-A_allele-1': '', 'HLA-A_allele-2': '', 'HLA-B_allele-1': '', 'HLA-B_allele-2': '', 'HLA-Bw_allele-1': '', 'HLA-Bw_allele-2': '', 'HLA-Cw_allele-1': '', 'HLA-Cw_allele-2': '', 'HLA-DRB1_allele-1': '', 'HLA-DRB1_allele-2': '', 'HLA-DRB3_allele-1': '', 'HLA-DRB3_allele-2': '', 'HLA-DRB4_allele-1': '', 'HLA-DRB4_allele-2': '', 'HLA-DRB5_allele-1': '', 'HLA-DRB5_allele-2': '', 'HLA-DQA1_allele-1': '', 'HLA-DQA1_allele-2': '', 'HLA-DQB1_allele-1': '', 'HLA-DQB1_allele-2': '', 'action': '/hla/save_new_patient'} 
  #keys_section='`'+'`,`'.join(post_dict.keys())+'`'
  #values_section='"'+'","'.join(post_dict.values())+'"'
  
  #log_and_display(keys_section,1)
  #log_and_display(values_section,1)
  
  
  start_sql=' update  donor set '
  mid_sql=''
  
  for i in post_dict.keys():
    mid_sql=mid_sql+' `{}`="{}" , '.format(i,post_dict[i])
    
  mid_sql=mid_sql[:-2]
  end_sql=' where `patient_id`="{}" '.format(pid) 
  sql=start_sql+mid_sql+end_sql
  log_and_display("update sql:{}".format(sql),1)
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  cur=m.run_query(con,prepared_sql=sql,data_tpl=None)

  
  html_data={
    #'post_dict':post_dict,
    'last_message':m.last_message,
    'collection_string':collection_string,
    'pid':pid,
    'uname':uname,
    'psw':psw
  }
  
  m.close_cursor(cur)
  m.close_link(con)
  #return template("temp.html",html_data=html_data)  
  return template("save_new_donor.html",html_data)  



@route('/save_edited_recipient', method='POST')
@decorate_verify_user
def save_edited_recipient():
  global collection_string
  collection_string=''
  post_dict=dict(request.forms.items())
  
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  pid=request.forms.get("patient_id")
   
  log_and_display('post data before removing unncessary post values:{}'.format(post_dict),1)
  post_dict.pop("action")
  post_dict.pop("uname")
  post_dict.pop("psw")
  post_dict.pop("patient_id")


  log_and_display('post data AFTER removing unncessary post values:{}'.format(post_dict),1)

  
  start_sql=' update  recipient set '
  mid_sql=''
  
  for i in post_dict.keys():
    mid_sql=mid_sql+' `{}`="{}" , '.format(i,post_dict[i])
    
  mid_sql=mid_sql[:-2]
  end_sql=' where `patient_id`="{}" '.format(pid) 
  sql=start_sql+mid_sql+end_sql
  log_and_display("update sql:{}".format(sql),1)
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  cur=m.run_query(con,prepared_sql=sql,data_tpl=None)

  
  html_data={
    #'post_dict':post_dict,
    'last_message':m.last_message,
    'collection_string':collection_string,
    'pid':pid,
    'uname':uname,
    'psw':psw
  }
  
  m.close_cursor(cur)
  m.close_link(con)
  #return template("temp.html",html_data=html_data)  
  return template("save_new_recipient.html",html_data)  




@route('/save_new_recipient', method='POST')
@decorate_verify_user
def save_new_recipient():

  post_dict=dict(request.forms.items())
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  pid=request.forms.get("patient_id")
  
  logging.debug(post_dict)
  post_dict.pop("action")
  post_dict.pop("uname")
  post_dict.pop("psw")
  logging.debug(post_dict)
  
  #{'patient_id': '1234', 'name': 'ok kjj', 'ABO': 'A', 'Rh': 'Positive', 'HLA-A_allele-1': '', 'HLA-A_allele-2': '', 'HLA-B_allele-1': '', 'HLA-B_allele-2': '', 'HLA-Bw_allele-1': '', 'HLA-Bw_allele-2': '', 'HLA-Cw_allele-1': '', 'HLA-Cw_allele-2': '', 'HLA-DRB1_allele-1': '', 'HLA-DRB1_allele-2': '', 'HLA-DRB3_allele-1': '', 'HLA-DRB3_allele-2': '', 'HLA-DRB4_allele-1': '', 'HLA-DRB4_allele-2': '', 'HLA-DRB5_allele-1': '', 'HLA-DRB5_allele-2': '', 'HLA-DQA1_allele-1': '', 'HLA-DQA1_allele-2': '', 'HLA-DQB1_allele-1': '', 'HLA-DQB1_allele-2': '', 'action': '/hla/save_new_patient'} 
  keys_section='`'+'`,`'.join(post_dict.keys())+'`'
  values_section='"'+'","'.join(post_dict.values())+'"'
  sql='insert into  recipient ('+keys_section+') values ('+values_section+')'
  logging.debug("insert sql:{}".format(sql))
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  cur=m.run_query(con,prepared_sql=sql,data_tpl=())
  m.close_link(con)
  return template("save_new_recipient.html",post_dict=post_dict,last_message=m.last_message,psw=psw,pid=pid,uname=uname,patient_id=pid)  

def select_query_get_first_row(sql,data_tpl):
  logging.debug("complate_a_query(sql,data_tpl) SQL={}".format(sql))
  logging.debug("complate_a_query(sql,data_tpl) data_tpl={}".format(data_tpl))
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  patient_data=m.get_single_row(cur)
  field_names = [i[0] for i in cur.description]
  logging.debug("fields={}".format(field_names))
  logging.debug("data={}".format(patient_data))
  if(patient_data==None):
    return None
  data_dict=dict(zip(field_names,patient_data))
  logging.debug("data_dict={}".format(data_dict))
  m.close_link(con)
  return data_dict
def select_query_get_all_rows(sql,data_tpl):
  logging.debug("complat((67185,), (112557,), (344413,), (383627,), (432571,), (437325,), (437835,), (440695,), (444619,), (444889,), (456979,), (457635,), (460609,), (462863,), (469921,), (473481,), (474547,), (475393,), (483313,), (492087,), (495309,), (497983,), (498735,), (498919,), (502249,), (502317,), (517601,))e_a_query(sql,data_tpl) SQL={}".format(sql))
  logging.debug("complate_a_query(sql,data_tpl) data_tpl={}".format(data_tpl))
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  patient_data=m.get_all_rows(cur)
  logging.debug("data={}".format(patient_data))
  m.close_link(con)
  return patient_data
   

def analyse_file_data(file_data):
  sn=''
  batch=''
  protocol_name=''
  next_line_is=''
  median_keys=[]
  median_data_of_one_patient={}
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  for each_line in file_data:
    if (len(each_line)==0):
      next_line_is=''
      logging.debug("#####empty line found")
      logging.debug("#####Data section ends here")
    elif(len(each_line)==2):
      #logging.debug("each_line:{}".format(each_line))    
      if(each_line[0]=='SN'):
        logging.debug("####serial number of equipment is:{}".format(each_line[1]))
        sn=each_line[1]
      elif(each_line[0]=='Batch'):
        logging.debug("####Batch ID is:{}".format(each_line[1]))
        batch=each_line[1]
      elif(each_line[0]=='ProtocolName'):
        logging.debug("####Protocol Name is:{}".format(each_line[1]))
        protocol_name=each_line[1]   
      elif(each_line[0]=='DataType:' and each_line[1]=='Median'):
        logging.debug("#####Median DataType is found")
        next_line_is='median_keys'
    elif (next_line_is=='median_keys'):
      next_line_is='median_data'
      logging.debug("next_line_is={}".format(next_line_is))
      median_keys=each_line
      logging.debug("median keys are:{}".format(median_keys))
    elif (next_line_is=='median_data'):
      #logging.debug("median data are:{}".format(each_line))
      unique_string=sn+'|'+batch+'|'+protocol_name
      median_data_of_one_patient=dict(zip(median_keys,each_line))
      patient_detail=median_data_of_one_patient['Sample'].split()
      logging.debug("patient details are :{}".format(patient_detail))
      if(len(patient_detail)!=3):
        logging.debug("patient details are not having three parts:{}".format(patient_detail))
        continue
      patient_id=patient_detail[2]
      logging.debug("median data of one patient is: {}".format(median_data_of_one_patient))
      sql='insert into recipent_antibodies \
              (patient_id,unique_string,antigen_id,mfi) values \
              (%s,%s,%s,%s) \
              on duplicate key update \
              mfi=%s '
              
              #where patient_id=%s and unique_string=%s and antigen_id=%s'
   
      for each_value_key_pair in median_data_of_one_patient.keys():
        
        if(each_value_key_pair.isdigit()==True):
          data_tpl=(patient_id,unique_string,each_value_key_pair,median_data_of_one_patient[each_value_key_pair],
          median_data_of_one_patient[each_value_key_pair])
          #,patient_id,unique_string,each_value_key_pair)
          logging.debug("data to be inserted/updated{}".format(data_tpl))
          try:
            cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
            m.close_cursor(cur)
          except Exception as ex:
            logging.debug('Error:::::{}'.format(ex))
            return False      
  m.close_link(con)          


#In use
#SAB search - original , based on recipient_antibodies,
@route('/search_SAB_database', method='POST')
@decorate_verify_user
def search_SAB_database_old():
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  pid=request.forms.get("patient_id")
  donor_data=select_query_get_first_row(
      sql='select * from donor where patient_id=%s',data_tpl=(pid,))

  if(donor_data==None):
    return "<h3>No donor data found for such patient id</h3>"
    logging.debug("No donor data found for such patient id")


  def make_string(donor_data):
    donor_data_string=()
    for fld in donor_data.keys():
      if(fld[:3]=='HLA'):
        if(len(donor_data[fld])>0):
          d1=fld.split("-")[1].split("_")[0]+"*"+donor_data[fld]
          donor_data_string=donor_data_string+(d1,)
    return donor_data_string    
    
  donor_data_tuple=make_string(donor_data)
  
  recipient_data=select_query_get_all_rows(
          sql='select patient_id,ABO,Rh,name from recipient where \
          (ABO=%s or ABO="AB") and (Rh=%s or Rh="Positive") ',data_tpl=(donor_data['ABO'],donor_data['Rh']))
  
  logging.debug("first data:{}".format(recipient_data[0][0]))
  antibody_data=select_query_get_all_rows(
                  sql="select * from recipient_antibodies \
                  where patient_id=%s",data_tpl=(recipient_data[0][0],)
                  )
  
  grand_data={}             
  for each_recipient_data in recipient_data:
    one_pt_data=()
    for each_donor_data in donor_data_tuple:
      one_filtered_rab=select_query_get_all_rows(
                    sql="select patient_id,antigen_id,HLA_Type,mfi from recipient_antibodies \
                    where patient_id=%s and locate(%s,HLA_Type)>0",
                    data_tpl=(each_recipient_data[0],each_donor_data))
      logging.debug("{}:{}".format(each_donor_data,one_filtered_rab))
      one_pt_data=one_pt_data+one_filtered_rab
    grand_data[each_recipient_data[0]]=one_pt_data 
    
  analysed_data=analyse_recipient_data(grand_data)
  return template("search_SAB_database.html", 
      pid=request.forms.get("patient_id"),
      donor_data=donor_data,
      recipient_data=recipient_data,
      antibody_data=antibody_data,
      donor_data_string=donor_data_tuple,
      grand_data=grand_data,
      uname=uname,
      psw=psw,
      analysed_data=analysed_data)



def analyse_recipient_data(recipient_data):
    return recipient_data



#this was used for anaysing full CSV type of import
@route('/search_SAB_database_full_csv', method='POST')
@decorate_verify_user
def search_SAB_database_full_csv_type():
  uname=request.forms.get("uname")
  psw=request.forms.get("psw")  
  pid=request.forms.get("patient_id") #donor id



  def make_string(donor_data):
    donor_data_string=()
    for fld in donor_data.keys():
      if(fld[:3]=='HLA'):
        if(len(donor_data[fld])>0):
          d1=fld.split("-")[1].split("_")[0]+"*"+donor_data[fld]
          donor_data_string=donor_data_string+(d1,)
    return donor_data_string  
      
  #####DONOR
  donor_data=select_query_get_first_row(
      sql='select * from donor where patient_id=%s',data_tpl=(pid,))

  if(donor_data==None):
    return "<h3>No donor data found for such patient id</h3>"
    logging.debug("No donor data found for such patient id")
    #can not go ahead if donor not available in database
      
  ######RECIPIENT
  recipient_data=select_query_get_all_rows(
          sql='select patient_id,ABO,Rh,name from recipient where \
          (ABO=%s or ABO="AB") and (Rh=%s or Rh="Positive") ',data_tpl=(donor_data['ABO'],donor_data['Rh']))

  ########all_ABO_matched_recipient_data antibody for class I and class II
  
  hla_1_align={
            'f27':['HLA-A_allele-1','HLA-A_allele-2'],
            'f32':['HLA-B_allele-1','HLA-B_allele-2'],
            }


  hla_2_align={            
            'f22':[ 'HLA-DRB1_allele-1','HLA-DRB1_allele-2',
                    'HLA-DRB3_allele-1','HLA-DRB3_allele-2',
                    'HLA-DRB4_allele-1','HLA-DRB4_allele-2',
                    'HLA-DRB5_allele-1','HLA-DRB5_allele-2'],
            'f28':[ 'HLA-DQA1_allele-1','HLA-DQA1_allele-2'],                        
            'f33':[ 'HLA-DQB1_allele-1','HLA-DQB1_allele-2'],                                                
            }

  hla_1_id={
            'f27':['A*'],
            'f32':['B*'],
            }


  hla_2_id={            
            'f22':[ 'DRB1*','DRB3*','DRB4*','DRB5*'],
            'f28':[ 'DQA1*'],                                                
            'f33':[ 'DQB1*'],                                                

            }
 
  all_ABO_matched_recipient_data_1=()
  all_ABO_matched_recipient_data_2=()
  all_mfi_ABO_matched_recipient_data_1=()
  all_mfi_ABO_matched_recipient_data_2=()
  
  for one_recipient_data in recipient_data:
    
    antibody_1_data=select_query_get_all_rows(
                  sql="select * from single_antigen_1_csv_report \
                  where patient_id=%s",data_tpl=(one_recipient_data[0],)
                  )
    all_ABO_matched_recipient_data_1=all_ABO_matched_recipient_data_1+ (antibody_1_data,)
    
    antibody_2_data=select_query_get_all_rows(
                  sql="select * from single_antigen_2_csv_report \
                  where patient_id=%s",data_tpl=(one_recipient_data[0],)
                  )
    all_ABO_matched_recipient_data_2=all_ABO_matched_recipient_data_2+(antibody_2_data,)


############relevent MFI for all_ABO_matched_recipient_data antibody for class I and class II
#MariaDB [(none)]> select sysdate() where 'gfd' in ('gfd','dsfsd');

    for each_hla in hla_1_align:
      hla_fields=str(hla_1_align[each_hla]).replace('[','').replace(']','').replace("'","`")
      hla_fields_for_in=str(hla_1_align[each_hla]).replace('[','').replace(']','').replace("'","`")
      hla_id_for_in=str(hla_1_id[each_hla]).replace('[','').replace(']','')
      mfi_sql="""
                  select 
                    *,{},substring(trim({}),1,2),
                    substring(trim({}),3),
                  {}
                  from 
                    donor d,single_antigen_1_csv_report r
                  where 
                    d.patient_id={} and 
                    r.patient_id={} and
                    substring(trim({}),1,2)in ({}) and
                    
                    substring(trim({}),3) in ({})
                  ;
          """.format(each_hla,each_hla,each_hla,hla_fields,
                    pid,one_recipient_data[0],each_hla,hla_id_for_in,each_hla,hla_fields_for_in)
      logging.debug("===========SQL=================")
      logging.debug(mfi_sql)
      logging.debug("===========end of SQL=================")
       
      mfi_antibody_1_data=select_query_get_all_rows(sql=mfi_sql,data_tpl=None)
      all_mfi_ABO_matched_recipient_data_1=all_mfi_ABO_matched_recipient_data_1+ (mfi_antibody_1_data)
            
            
    for each_hla in hla_2_align:
      hla_fields=str(hla_2_align[each_hla]).replace('[','').replace(']','').replace("'","`")
      hla_fields_for_in=str(hla_2_align[each_hla]).replace('[','').replace(']','').replace("'","`")
      hla_id_for_in=str(hla_2_id[each_hla]).replace('[','').replace(']','')
      mfi_sql="""
                  select 
                    *,{},substring(trim({}),1,2),
                    substring(trim({}),3),
                  {}
                  from 
                    donor d,single_antigen_2_csv_report r
                  where 
                    d.patient_id={} and 
                    r.patient_id={} and
                    substring(trim({}),1,2) in ({}) and
                    
                    substring(trim({}),3) in ({})
                  ;
          """.format(each_hla,each_hla,each_hla,hla_fields,
                    pid,one_recipient_data[0],each_hla,hla_id_for_in,each_hla,hla_fields_for_in)
      logging.debug("===========SQL2=================")
      logging.debug(mfi_sql)
      logging.debug("===========end of SQL2=================")
       
      mfi_antibody_2_data=select_query_get_all_rows(sql=mfi_sql,data_tpl=None)
      all_mfi_ABO_matched_recipient_data_2=all_mfi_ABO_matched_recipient_data_2+ (mfi_antibody_2_data)
            
            
  logging.debug(all_mfi_ABO_matched_recipient_data_1)
  logging.debug(all_mfi_ABO_matched_recipient_data_2)                    
   
  return template("search_SAB_database.html", 
      pid=request.forms.get("patient_id"),
      uname=uname,
      psw=psw,
      donor_data=donor_data,
      recipient_data=recipient_data,
      all_ABO_matched_recipient_data_1=all_ABO_matched_recipient_data_1,      
      all_ABO_matched_recipient_data_2=all_ABO_matched_recipient_data_2,
      all_mfi_ABO_matched_recipient_data_1=all_mfi_ABO_matched_recipient_data_1,
      all_mfi_ABO_matched_recipient_data_2=all_mfi_ABO_matched_recipient_data_2)

'''


select 
trim(`HLA-A_allele-1`),
trim(`HLA-A_allele-2`),
f27,substring(trim(f27),1,2),
substring(trim(f27),3),
if(trim(`HLA-A_allele-1`)=substring(trim(f27),1,2),'match','not match')


from 

donor d,single_antigen_1_csv_report s 


where 
d.patient_id=517601 and 
s.patient_id=444444 and
substring(trim(f27),1,2)='A*'
;

=============


select 
*,
f27,substring(trim(f27),1,2),
substring(trim(f27),3),
if(trim(`HLA-A_allele-1`)=substring(trim(f27),1,2),'match','not match')


from 

donor d,single_antigen_1_csv_report s 


where 
d.patient_id=517601 and 
s.patient_id=444444 and
substring(trim(f27),1,2)='A*'
;

=============


select 
*,
f27,substring(trim(f27),1,2),
`HLA-A_allele-1`,
`HLA-A_allele-2`,
substring(trim(f27),3),
if(trim(`HLA-A_allele-1`)=substring(trim(f27),3),'match','not match'),
if(trim(`HLA-A_allele-2`)=substring(trim(f27),3),'match','not match')

from 

donor d,single_antigen_1_csv_report s 


where 
d.patient_id=517601 and 
s.patient_id=444444 and
substring(trim(f27),1,2)='A*'
;

================final==================
select 
*,
f27,substring(trim(f27),1,2),
`HLA-A_allele-1`,
`HLA-A_allele-2`,
substring(trim(f27),3),
if(trim(`HLA-A_allele-1`)=substring(trim(f27),3),'match','not match'),
if(trim(`HLA-A_allele-2`)=substring(trim(f27),3),'match','not match')

from 

donor d,single_antigen_1_csv_report s 


where 
d.patient_id=517601 and 
s.patient_id=444444 and
substring(trim(f27),1,2)='A*' and
trim(`HLA-A_allele-2`)=substring(trim(f27),3)
;
===================end of final============



data matching

hla_1_align={
            'f27':['HLA-A_allele-1','HLA-A_allele-2'],
            'f32':['HLA-B_allele-1','HLA-B_allele-2'],
            }


hla_2_align={            
            'f22':[ 'HLA-DRB1_allele-1','HLA-DRB1_allele-2',
                    'HLA-DRB3_allele-1','HLA-DRB3_allele-2',
                    'HLA-DRB4_allele-1','HLA-DRB4_allele-2',
                    'HLA-DRB5_allele-1','HLA-DRB5_allele-2'],
            'f28':[ 'HLA-DQA1_allele-1','HLA-DQA1_allele-2'],                        
            'f33':[ 'HLA-DQB1_allele-1','HLA-DQB1_allele-2'],                                                
            }
            
            

'''
