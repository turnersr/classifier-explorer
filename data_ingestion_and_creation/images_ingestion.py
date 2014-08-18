# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os, re, sys
import pandas as pd
from IPython.parallel import Client
PATH = '/mnt/data/nfp_bk/nfp3/'
zillow = pd.read_csv(PATH+'zillow_data/zillow.csv')
zipcodes = pd.read_csv(PATH+'zillow_data/zipcode_latlong.csv')
rc = Client()
view = rc[:]

# <codecell>

nyboston_zips = zipcodes['zipcode'].tolist()
zillow_nyboston = zillow[zillow['RegionName'].isin(nyboston_zips)]

# <codecell>

years = list(zillow_nyboston.columns[5:])
neighborhoods = zillow_nyboston[years]
neighborhoods = pd.DataFrame(neighborhoods[neighborhoods.columns[1:]].mean(axis=1))
neighborhoods.columns = ['mean_valuation']
neighborhoods['zipcode'] = zillow_nyboston['RegionName']
neighborhoods.sort(columns=['mean_valuation'])

# <codecell>

## will be abstracted away later such that input zipcodes and populate relevant directories ## 
poor_zipcode = 10462
rich_zipcode  = [10013,10007,10065]

rich_latlong = zipcodes[zipcodes['zipcode'].isin(rich_zipcode)]
rich_latlong['label'] = 1

poor_latlong = zipcodes[zipcodes['zipcode']==poor_zipcode]
poor_latlong['label'] = 0

latlong = pd.concat([poor_latlong,rich_latlong])

# <codecell>

def get_url(x,heading):
    dim = (231,231)
    latitude = x[0]
    longitude = x[1]
    base_url = "http://maps.googleapis.com/maps/api/streetview?size=%dx%d&location=%f,%f&heading=%f&pitch=%f&key=AIzaSyBZBHzMBCtplYvXCeg1NbdIJc8MpIXR-4U" %(dim[0],dim[1],latitude,longitude, heading,0)
    return base_url

def image_samples(csv_file=latlong,heading=0):
    indices = [0,1,2]
    image_stats = []
    for row in csv_file.iterrows():  
        row_stats = [row[1][i] for i in indices]
        lat,lon = row_stats[0:2]
        row_stats.append(get_url((lat,lon),0))
        image_stats.append(row_stats)
    
    return image_stats


def image_ingestion(image_stats,path=PATH,header=0):
    """
    puts sample images in test directory
    """
    import os,sys
    lat,lon,zipcode,url = image_stats
    file_name = "'image_"+str(lat)+str(lon)+str(zipcode)+"_"+ str(header)+".jpeg' "
    cmd = 'sudo wget -O ' + file_name+ "'"+str(url) + "'"
    dir_path = path + 'test_images/' + str(int(zipcode))

    if not os.path.exists(dir_path):
        dir_cmd = 'sudo mkdir ' + dir_path
        os.system(dir_cmd)

    os.chdir(dir_path)
    os.system(cmd)
    return 1
    
             
        

# <codecell>

%timeit images_ingested = view.map_sync(image_ingestion,image_samples())

