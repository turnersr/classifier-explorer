#! /bin/bash

DL=../../datasets/url_queries/
wget -o boston_urls.tar.gz --no-check-certificate https://www.dropbox.com/s/yaif7peyu65n79s/boston_urls.tar.gz
mkdir -p $DL
tar -vxzf boston_urls.tar.gz -C $DL
rm boston_urls.tar.gz

