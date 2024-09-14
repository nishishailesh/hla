#!/bin/bash
echo "Give name of HLA database:"
read d
mysqldump  -d $d > cl_general_blank_2023.sql 
tnames='
antigen
'
mysqldump  $d $tnames > "cl_general_data_2023.sql"


git add *
git commit -a
git push https://github.com/nishishailesh/hla main

