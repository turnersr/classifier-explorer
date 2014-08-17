#! /bin/bash
wget https://www.dropbox.com/sh/5b9ibj8shii2q5v/AAADK8DLKeg2rFyYEjJ_afWXa/newyorkcity_urls.tar.gz
mkdir -p url_queries/
tar -vxzf newyorkcity_urls.tar.gz -C url_queries
rm newyorkcity_urls.tar.gz

