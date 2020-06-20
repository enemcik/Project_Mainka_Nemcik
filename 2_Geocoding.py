import pandas as pd
import numpy as np
import json
import os
import math
import geopy
import geopandas as gpd
from geopy.extra.rate_limiter import RateLimiter
import platform

fileDir = os.path.dirname(os.path.realpath('__file__'))

def data_combine(*args):
    '''loads stored JSON files and combines them into one big dictionary'''
    big_dict = []
    data = {}
    #input example - 'idnes_reality.json', 'bezrealitky.json'
    for arg in args:
        if system.platform() == 'Darwin':
            with open(fileDir + '/Data/' + arg) as json_file:
                file_ = json.load(json_file)
                big_dict.append(file_)
        else:
            with open(fileDir + '\\Data\\' + arg) as json_file:
                file_ = json.load(json_file)
                big_dict.append(file_)
    for dt in big_dict:
        data.update(dt)
    return data

data = data_combine('bezrealitky.json', 'idnes_reality.json') 

def clean_dataframe(data_file):
    '''
    The clean_dataframe function takes a data file (here a dictionary) as an input and returns a pandas dataframe, which is cleaned up and ready to use. 
    In particular, NaN values are replaced with nothing, white spaces before and after strings in the columns which have strings are removed 
    (which is important for the duplicate search), Rows which are duplicates (ergo same flat) are removed, the removal is executed based on the columns
    Size, m2, Street and Total Price as it is highly likely that in case flats are exactly identical in these values the flat is identical and a new column 'Address'
    is created which is necessary for geocoding.
    '''
    df = pd.DataFrame(data_file).T
    df = df.replace('NaN', '', regex=True)
    for name in ['Size','Street','District']: #strips all white spaces before and after strings
        df[name]=df[name].str.strip()
    print('Number of (removed) duplicates: ' + str(df.duplicated(['Size', 'm2', 'Street', 'Total Price']).sum()))
    df = df.drop_duplicates(['Size', 'm2', 'Street', 'Total Price'], ignore_index=True) #drops duplicates 
    df['Address'] = df['Street'] + ',' + df['District'] + ',' + 'Praha' #creating address column for geocoding
    return df

dataframe = clean_dataframe(data)


### Geocoding

locator = geopy.Nominatim(user_agent='myGeocoder')

#getting the GPS addresses
geocode = RateLimiter(locator.geocode, min_delay_seconds=1) #this process takes about 2,5 hours

'''We use Nominatim, an open source geocoding provider to retrive the locations (latitude, longitude, altitude) for our apartments. 
For this we provide Nominatim with the addresses of the aparments. Through the address, practically a "Google Maps search" is conducted and 
the latitude, longitude, altitude for the address is returned.'''

dataframe['location'] = dataframe['Address'].apply(geocode)

dataframe['point'] = dataframe['location'].apply(lambda loc: tuple(loc.point) if loc else None)

dataframe[['latitude', 'longitude', 'altitude']] = pd.DataFrame(dataframe['point'].tolist(), index=dataframe.index)

dataframe = dataframe.dropna()
if platform.system() == 'Darwin':
    dataframe.to_pickle(fileDir + '/Data/' + 'geo_df.pkl', protocol = 4)
else:
    dataframe.to_pickle(fileDir + '\\Data\\' + 'geo_df.pkl', protocol = 4)


