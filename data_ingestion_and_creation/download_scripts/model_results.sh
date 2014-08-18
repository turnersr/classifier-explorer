#! /bin/bash
DL=../../datasets/model_results/
wget -O results.tar.gz --no-check-certificate https://www.dropbox.com/s/2h92u7hh12pvhi0/results.tar.gz
mkdir -p $DL
tar -vxzf results.tar.gz -C $DL
rm results.tar.gz
