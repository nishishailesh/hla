#HLA single antigen recipient database search for MFI related to donor HLA
- mod_wsgi needs to be installed for apache2 based installation 
- Following python modules are also required. Install related packages
  - from bottle import template, request, post, route, redirect
  - from datetime import datetime
  - from mysql_lis import mysql_lis
  - import sys, logging, bcrypt, csv, pprint
  - from functools import wraps
  - from io import StringIO
- edit apache2.for.hla.conf for paths (common WSGI declaration may have to be commented if used somewhere)
- point astm_var module to appropriate file. Also supply its location in index.py
  - the location folder must have +x +r permission
- update path in wsgi.py to point to installation folder
- use python3 commands described in verify_login() to generate password
- touch /var/log/hla.log and chmod www-data:www-data

