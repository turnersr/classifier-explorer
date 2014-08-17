#! /bin/bash
wget https://www.dropbox.com/s/oz8uv312rvlqx0a/500_images.tar.gz
mkdir test_images
tar -vxzf 500_images.tar.gz -C test_images
rm 500_images.tar.gz
