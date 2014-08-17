# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os, re, math, time, pickle, csv
import pandas as pd
import numpy as np
from collections import Counter

# <codecell>

zillow_valuation = pd.read_csv('zillow_data/zillow.csv')
boston = pd.read_csv('zillow_data/streetscore_boston.csv')
newyork = pd.read_csv('zillow_data/streetscore_newyorkcity.csv')
zip_codes = pd.read_csv('zillow_data/cityzip.csv')
coordinates = []
zips = dict()
for item in boston.iterrows():
    lat,lon = item[1][0],item[1][1]
    coordinates.append((lat,lon))
for item in newyork.iterrows():
    lat,lon = item[1][0],item[1][1]
    coordinates.append((lat,lon))

for item in zip_codes.iterrows():
    zip_code,lat,lon =  int(item[1][2]),float(item[1][3]),float(item[1][4])
    zips[(lat,lon)] = zip_code 

# <codecell>

rc = Client()
view = rc[:]
view['zips'] = zips
@view.parallel(block=True)
def coords2zipcode(coords):
    """
    input: (lat,long)
    output: nearest zipcode 
    """
    import math 
    lat,lon = coords
    MIN_DISTANCE = 100000
    MIN_KEYS = None
    for zip_lat,zip_lon in zips.keys():
        distance = math.hypot(zip_lat-lat,zip_lon-lon)
        if distance < MIN_DISTANCE:
            MIN_DISTANCE = distance
            MIN_KEYS = zip_lat,zip_lon
            
    if MIN_KEYS:
        zipcode = zips[MIN_KEYS]
        return lat,lon,zipcode
    else:
        print coords
        return "No Relevant Zip Code Found"

# <codecell>

%time zipcodes = coords2zipcode.map(coordinates)

# <codecell>

with open('zipcode_latlong.csv','w') as f:
    zip_csv = csv.writer(f)
    zip_csv.writerow(['latitude','longitude','zipcode'])
    for row in zipcodes:
        zip_csv.writerow(row)

