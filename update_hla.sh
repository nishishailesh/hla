#!/bin/bash
echo "Give name of HLA database:"
read d
mysqldump  -d $d > "hla_blank.sql"

git add *
git commit -a
git push https://github.com/nishishailesh/hla main

