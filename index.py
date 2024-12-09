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

@route('/import_SAB_plate_csv', method='POST')
@decorate_verify_user
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
@decorate_verify_user
def get_patient_detail():
    uname=request.forms.get("uname")
    psw=request.forms.get("psw")
    return template("get_patient_detail.html",uname=uname,psw=psw)

@route('/view_patient_detail', method='POST')
@decorate_verify_user
def view_patient_detail():
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
    return "<h3>No donor data found for such donor id</h3>"
    logging.debug("No donor data found for such donor id")
  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  data_dict=dict(zip(field_names,patient_data))
  logging.debug("data_dict:{}".format(data_dict))
  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict
  }
  print(data_dict)
  return template("view_patient_detail.html",html_data)
  
@route('/view_recipient_detail', method='POST')
@decorate_verify_user
def view_recipient_detail():
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)
  patient_id=request.forms.get("patient_id")
  sql='select * from recipient where patient_id=%s'
  logging.debug("sql:{}".format(sql))
  data_tpl=(patient_id,)
  logging.debug("data_tpl:{}".format(data_tpl))
  cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
  logging.debug("last_message{}".format(m.last_message))
  patient_data=m.get_single_row(cur)
  logging.debug("patient_data:{}".format(patient_data))


  if(patient_data==None):
    return "<h3>No recipient data found for such patient id</h3>"
    logging.debug("No recipient data found for such patient id")

  
  num_fields = len(cur.description)
  field_names = [i[0] for i in cur.description]  
  logging.debug("field_names:{}".format(field_names))
  data_dict=dict(zip(field_names,patient_data))
  logging.debug("data_dict:{}".format(data_dict))
  m.close_link(con)
  html_data={
  'patient_id':request.forms.get("patient_id"),
  'last_message':m.last_message,
  'patient_data':patient_data,
  'data_dict':data_dict
  }
  print(data_dict)
  return template("view_patient_detail.html",html_data)
  

@route('/save_new_patient', method='POST')
@decorate_verify_user
def save_new_patient():
  post_dict=dict(request.forms.items())
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
  return template("save_new_patient.html",post_dict=post_dict,last_message=m.last_message)  

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


@route('/search_SAB_database', method='POST')
@decorate_verify_user
def search_SAB_database():
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
  return template("search_SAB_database.html", 
      pid=request.forms.get("patient_id"),
      donor_data=donor_data,recipient_data=recipient_data,
      antibody_data=antibody_data,
      donor_data_string=donor_data_tuple,
      grand_data=grand_data,uname=uname,psw=psw)

  
