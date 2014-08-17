
# coding: utf-8

# In[99]:

import pandas as pd
import time
import csv


# In[100]:

def get_url(x,heading):
    latitude = x[0]
    longitude = x[1]
    base_url = "http://maps.googleapis.com/maps/api/streetview?size=256x256&location=%f,%f&heading=%f&pitch=%f&key=AIzaSyBZBHzMBCtplYvXCeg1NbdIJc8MpIXR-4U" %(latitude,longitude, heading,0)
    return base_url


# In[101]:

def create_url_col(x, outfile):
    for heading in range(0,360,45):
        x["heading_%d" % heading] = x.apply(get_url,heading=heading,axis=1)
    x.to_csv(outfile,index=False, sep='\t', quoting=csv.QUOTE_MINIMAL)
    


# In[102]:

mappping = {"/mnt/data/nfp_bk/nfp3/streetscore_dataset/streetscore_boston.csv":"boston_urls.csv",
            "/mnt/data/nfp_bk/nfp3/streetscore_dataset/streetscore_newyorkcity.csv":"newyorkcity_urls.csv" }

def create_url_queries(lat_long_file_to_outfile):
    for infile, outfile in lat_long_file_to_outfile.items():
        df = pd.read_csv(infile)
        x = df[["latitude","longitude"]]
        create_url_col(x,outfile)


# In[103]:

create_url_queries(mappping)


# In[98]:

list(x.heading_0)[0:100]
