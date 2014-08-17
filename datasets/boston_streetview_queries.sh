#! /bin/bash
wget https://www.dropbox.com/s/yaif7peyu65n79s/boston_urls.tar.gz
mkdir -p url_queries/
tar -vxzf boston_urls.tar.gz -C url_queries
rm boston_urls.tar.gz

