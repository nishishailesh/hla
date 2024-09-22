#!/usr/bin/python3
#from bottle import route, run, template
from bottle import template, request, post, route, redirect
from datetime import datetime
from mysql_lis import mysql_lis
import sys, logging, bcrypt, csv
from io import StringIO

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

@route('/get_SAB_plate_csv', method='POST')
def get_SAB_plate_csv():
  return template("get_SAB_plate_csv.html")

@route('/import_SAB_plate_csv', method='POST')
def do_upload():
  upload= request.files.get('SAB_csv')
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

@route('/get_patient_detail', method='POST')
def get_patient_detail():
  return template("get_patient_detail.html")
  

def analyse_file_data(file_data):
  sn=''
  batch=''
  protocol_name=''
  next_line_is=''
  median_keys=[]
  median_data_of_one_patient={}
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
      logging.debug("median data of one patient is: {}".format(median_data_of_one_patient))
      



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
