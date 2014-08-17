#! /bin/bash
DL=../../datasets/
wget http://streetscore.media.mit.edu/static/files/streetscore_data.zip
mkdir -p $DL
unzip -o streetscore_data.zip -d $DL
rm streetscore_data.zip
