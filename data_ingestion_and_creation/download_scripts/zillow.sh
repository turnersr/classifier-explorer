#! /bin/bash
DL=../../datasets/zillow/
wget -o zillow.tar.gz --no-check-certificate https://www.dropbox.com/s/qvujla1o7dw2adg/zillow.tar.gz
mkdir -p $DL
tar -vxzf zillow.tar.gz -C $DL
rm zillow.tar.gz
