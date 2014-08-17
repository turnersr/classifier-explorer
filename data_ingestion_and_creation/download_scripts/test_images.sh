#! /bin/bash
DL=../../datasets/test_images/
wget -O 500_images.tar.gz --no-check-certificate https://www.dropbox.com/s/s7k3uz782fwgcen/500_images.tar.gz
mkdir -p $DL
tar -vxzf 500_images.tar.gz -C $DL
rm 500_images.tar.gz
