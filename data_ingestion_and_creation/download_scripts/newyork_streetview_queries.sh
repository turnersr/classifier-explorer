#! /bin/bash
DL=../../datasets/url_queries/
wget -o newyorkcity_urls.tar.gz --no-check-certificate https://www.dropbox.com/sh/5b9ibj8shii2q5v/AAADK8DLKeg2rFyYEjJ_afWXa/newyorkcity_urls.tar.gz
mkdir -p $DL
tar -vxzf newyorkcity_urls.tar.gz -C $DL
rm newyorkcity_urls.tar.gz

