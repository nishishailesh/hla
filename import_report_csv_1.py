#!/usr/bin/python3
#from bottle import route, run, template
from bottle import template, request, post, route, redirect
from datetime import datetime
from mysql_lis import mysql_lis
import sys, logging, bcrypt, csv, pprint
from functools import wraps
from io import StringIO
from index import log_and_display

#For mysql password
sys.path.append('/var/gmcs_config')
###########Setup this for getting database,user,pass for HLA database##########
import astm_var_hla as astm_var
##############################################################
logging.basicConfig(filename="/var/log/hla.log",level=logging.DEBUG) 


#patient_id	unique_string	antigen_id	mfi	HLA_Type
def save_imp_data_to_SAB(patient_id,unique_string,imp_data_list):
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db) 
  sql='insert into recipient_antibodies \
          (patient_id,unique_string,antigen_id,mfi,HLA_Type) values \
          (%s,%s,%s,%s,%s) \
          on duplicate key update \
          mfi=%s '
  #{'Antigen ID': ' 178', 'Raw Value': ' 12022', 'A': ' ', 'B': ' B*73:01'}
  for each_imp_dict in imp_data_list: 
    data_tpl=(patient_id,unique_string,
            each_imp_dict['Antigen ID'],
            each_imp_dict['Raw Value'],
            '{}/{}'.format(each_imp_dict['A'].strip(),each_imp_dict['B'].strip()),
            each_imp_dict['Raw Value']
            )

    logging.debug("data to be inserted/updated{}".format(data_tpl))
    try:
      cur=m.run_query(con,prepared_sql=sql,data_tpl=data_tpl)
      m.close_cursor(cur)
    except Exception as ex:
      logging.debug('Error:::::{}'.format(ex))
      return False      
  m.close_link(con)          

# Header is on line-17 (python [16])
#antigen starts from line-18 to line-113 [Python [17] to [112]
def save_report_csv_1_io(io_handle):
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  all_data=io_handle.read()
  #logging.debug("data-->{}".format(all_data))

  rd = csv.reader(StringIO(all_data.decode("UTF-8")), delimiter=',')
  rd_list=list(rd)
  #logging.debug("data-->{}".format(rd_list))

  line_counter=0
  field_names={}
  main_list_of_imp_data_dict=[]
  expected_batch_id_location=0
  for i in rd_list:
    log_and_display("Line number:{}".format(line_counter),1)

    #checking if class 1 (also useful to find index for bath id in next line
    if(line_counter==4):
      log_and_display("Line 4: Expecting class 1 string",1)
      class_1_string="Class I Single Antigen Results"
      try:
        class_1_string_index=i.index(class_1_string)
        log_and_display("Line 4: class 1 string index is {} and value is {}".format(class_1_string_index,i[class_1_string_index]),1)
        expected_batch_id_location=class_1_string_index
      except:
        log_and_display("Line 4: class 1 string index not found. Serious issue",1)

    #batch id
    if(line_counter==5):
      log_and_display("Line 5: Expecting Batch ID at position:{}".format(expected_batch_id_location),1)
      log_and_display("Line 5: expected batch location index is {} and value is {}".format(expected_batch_id_location,i[expected_batch_id_location]),1)
      batch_id=rd_list[5][expected_batch_id_location]
      log_and_display("actual Batch Id is:{}".format(batch_id),1)

    #patient id
    if(line_counter==6):
      patient_id_check_string='Patient Name:'
      log_and_display("Line 6: Expecting patient_id in this line:{}".format(i),1)
      if(patient_id_check_string==i[1]):
        log_and_display("Line 6, index 1 is looking good: {}".format(i[1]),1)
        log_and_display("Line 6, index 9 should be patient_id : {}".format(i[9]),1)
        patient_id_split=i[9].split("\t")
        if(len(patient_id_split)!=3):
          log_and_display("Length of patient_id_split field is:{}. Length must be 3".format(patient_id_split))
          log_and_display("import stopped!!!!")
          return False
        else:
          patient_id=patient_id_split[2]
        log_and_display("actual Patient ID after split is:{}".format(patient_id),1)

    #field names    
    if(line_counter==16):
      log_and_display(i,1)
      field_names=i
      log_and_display("Now antigen data will start from [17] to [112]",1)
      
    #antigen mfi data
    if(line_counter>=17 and line_counter<=112):
      log_and_display('list data:{}'.format(i),1)
      data_dict=dict(zip(field_names,i))
      log_and_display('dictionary data with fields:{}'.format(data_dict),1)
      imp_data_dict={}
      #['', '', '', '', '', 'Antigen ID', '', '', '', '', 'Cut-off', '', '', '', 'Raw Value', 'MFI/LRA', '', '', 'BG Adjusted', 'AD-MFI', '', 'AD-BG Adjusted', '', '', '', '', '', 'A', '', '', '', '', 'B', 'C', '', '', '', 'Bw', '', 'A Serology', '', '', '', '', 'B Serology', '', '', 'C Serology', '', 'RAD', '', 'Epitopes']
      keys_for_imp_data_dict=['Antigen ID','Raw Value','A','B']
      for key in  keys_for_imp_data_dict:
        if key in data_dict:
          imp_data_dict[key]=data_dict[key]
      log_and_display('important data dictionary with fields:{}'.format(imp_data_dict),1)
      main_list_of_imp_data_dict=main_list_of_imp_data_dict+[imp_data_dict]
    line_counter=line_counter+1
    
  log_and_display('main_list_of_imp_data_dict:{}'.format(main_list_of_imp_data_dict),1)
  m.close_link(con)
  save_imp_data_to_SAB(patient_id,batch_id,main_list_of_imp_data_dict)  
  
  return  patient_id




def save_report_csv_1(csv_file_name):
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
        
  logging.debug("Batch ID Index 5 field 23 field is:{}".format(rd_list[5][22]))
  batch_id=rd_list[5][23]

  line_counter=0
  for i in rd_list:
    logging.debug("Line number:{} is:{}".format(line_counter,i))
    i=[patient_id,batch_id, str(line_counter)] + i
    logging.debug(" string lenght count=:{}".format(len(i)))
    logging.debug("New Line after adding primary keys is :{}".format(i))
    values_section='"'+'","'.join(i)+'"'
    logging.debug(values_section)
    sql='insert into  single_antigen_1_csv_report values ('+values_section+')'
    logging.debug("insert sql:{}".format(sql))
    cur=m.run_query(con,prepared_sql=sql,data_tpl=[])
    line_counter=line_counter+1
  m.close_link(con)
    

#save_report_csv_1("x.csv")


'''
def save_report_csv_1_io(io_handle):
  m=mysql_lis()
  con=m.get_link(astm_var.my_host,astm_var.my_user,astm_var.my_pass,astm_var.my_db)   
  all_data=io_handle.read()
  #logging.debug("data-->{}".format(all_data))

  rd = csv.reader(StringIO(all_data.decode("UTF-8")), delimiter=',')
  rd_list=list(rd)
  #logging.debug("data-->{}".format(rd_list))

  logging.debug("Patient ID field line is :{}".format(rd_list[6]))
  logging.debug("Patient ID field in report is:{}".format(rd_list[6][9]))
  patient_id_split=rd_list[6][9].split("\t")

  if(len(patient_id_split)!=3):
    logging.debug("Length of patient_id_split field is:{}. Length must be 3".format(patient_id_split))
    logging.debug("import stopped!!!!")
    return False
  else:
    patient_id=patient_id_split[2]
  logging.debug("actual Patient ID after split is:{}".format(patient_id))
    

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
    logging.debug('value section:{}'.format(values_section))
    sql='insert into  single_antigen_1_csv_report values ('+values_section+')'
    logging.debug("insert sql:{}".format(sql))
    #cur=m.run_query(con,prepared_sql=sql,data_tpl=[])
    cur=m.run_query(con,prepared_sql=sql,data_tpl=None)
    line_counter=line_counter+1
  m.close_link(con)
  return  patient_id 
'''



