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



def save_report_csv(csv_file_name):    
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   

  f=open(csv_file_name,"r")
  rd = csv.reader(f, delimiter=',')
  rd_list=list(rd)

  logging.debug("Patient ID field line is :{}".format(rd_list[6]))
  logging.debug("Patient ID field in report is:{}".format(rd_list[6][9]))
  patient_id_split=rd_list[6][9].split("\t")
  if(len(patient_id_split)!=3):
    logging.debug("Length of patient_id_split field is:{}. Length must be 3".format(patient_id_split))
    logging.debug("import stopped!!!!")
    return False
  else:
    patient_id=patient_id_split[2]
    

  batch_id=rd_list[5][22]   #no further processing. Because it has nothing to do with HIMS data
    
  logging.debug("Batch ID field is:{}".format(rd_list[5][22]))
  batch_id=rd_list[5][22]

  line_counter=0
  for i in rd_list:
    logging.debug("Line number:{} is:{}".format(line_counter,i))
    i=[patient_id,batch_id, str(line_counter)] + i
    logging.debug(" string lenght count=:{}".format(len(i)))
    logging.debug("New Line after adding primary keys is :{}".format(i))
    values_section='"'+'","'.join(i)+'"'
    logging.debug(values_section)
    sql='insert into  single_antigen_csv_report values ('+values_section+')'
    logging.debug("insert sql:{}".format(sql))
    cur=m.run_query(con,prepared_sql=sql,data_tpl=[])
    line_counter=line_counter+1
  m.close_link(con)
    



save_report_csv("x.csv")
