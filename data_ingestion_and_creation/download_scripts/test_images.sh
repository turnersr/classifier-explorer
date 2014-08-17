#! /bin/bash
DL=../../datasets/test_images/
wget -o 500_images.tar.gz --no-check-certificate https://www.dropbox.com/s/oz8uv312rvlqx0a/500_images.tar.gz
mkdir -p $DL
tar -vxzf 500_images.tar.gz -C $DL
rm 500_images.tar.gz
