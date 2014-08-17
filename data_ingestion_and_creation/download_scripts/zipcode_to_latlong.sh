#! /bin/bash
DL=../../datasets/zipcode_latlong/
wget --no-check-certificate https://www.dropbox.com/s/zy1zpwbbrir3emu/zipcode_latlong.tar.gz
mkdir -p $DL
tar -vxzf zipcode_latlong.tar.gz -C $DL
rm zipcode_latlong.tar.gz
