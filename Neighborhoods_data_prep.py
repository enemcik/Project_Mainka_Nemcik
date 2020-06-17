#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json
import os
import math
import geopy
import geopandas as gpd


# In[2]:


fileDir = os.path.dirname(os.path.realpath('__file__'))


# In[3]:


class NeighborhoodsVisuals(): 
    def __init__(self, geo_filename='Praha.json', df_filename = 'geo_df.pkl'):
        '''
        NeighborhoodsVisuals takes a dataframe containing information about apartments and their geographic location and data (as a JSON file) 
        about the geographic location of Neighborhoods (here of Prague) as input and its methods combine this data, compute average values 
        for the neighborhoods and store them as a JSON file for later use. As an exeption we just manually downloaded the Praha.json file in this form from http://opendata.praha.eu/
        '''
        with open(fileDir + '\\Data\\' + geo_filename, encoding="utf8") as data: 
                        hoods = json.loads(data.read()) #open neighborhoods data file (JSON format)
        self.gdf = gpd.GeoDataFrame.from_features(hoods["features"])
        df = pd.read_pickle(fileDir + '\\Data\\' + df_filename) #open individual apartments file (PKL format)
        self.gdf_indv = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.longitude, df.latitude))
        self.avg_prices()
        self.store_merged()
                
    def avg_prices(self):
        '''
        Joins individual apartment geographic-dataframe with geographic-dataframe of neighborhoods and then calculates summary statistics for neighborhoods. 
        If called prints dataframe of summary statistics.
        '''
        df_ = gpd.sjoin(self.gdf_indv, self.gdf, op='within') 
        df_ = df_.loc(axis=1)['Size', 'm2', 'Street', 'District', 'Base Price', 'Address', 'location', 'latitude',
            'longitude', 'geometry', 'index_right', 'OBJECTID', 'PLOCHA', 'ID', 'NAZEV_MC',
            'KOD_MO', 'TID_TMMESTSKECASTI_P', 'NAZEV_1', 'Shape_Length', 'Shape_Area']
        df_["m2"] = df_['m2'].apply(pd.to_numeric)
        avg_price = df_.loc(axis=1)['NAZEV_MC','Base Price','m2'].groupby(['NAZEV_MC']).mean().round()
        avg_price['Median Price'] = df_.loc(axis=1)['NAZEV_MC','Base Price'].groupby(['NAZEV_MC']).median().round()
        avg_price['Crown per m2'] = (avg_price['Base Price'] / avg_price['m2']).round()
        avg_price['Number of Apartments'] = df_.loc(axis=1)['NAZEV_MC','Base Price'].groupby(['NAZEV_MC']).count()
        avg_price.columns = ['Price', 'm2', 'Median_price', 'Avg_m2_price', 'Number_of_Apartments']
        return avg_price
    
    def store_merged(self):
        '''Merges the geographic-dataframe of neighborhoods object with the neighborhood summary data from avg_prices'''
        merged = pd.merge(self.gdf, self.avg_prices(), on='NAZEV_MC', how='left')
        merged = merged.fillna(value={'Price': 0, 'm2': 0})
        json_data = json.dumps(json.loads(merged.to_json()))  # Convert to json preferred string-like object 
        with open(fileDir + '\\Data\\merged_visuals_data.json', 'w') as write_file: #store data into a json file
            json.dump(json_data, write_file, indent = 4)


# In[4]:


e = NeighborhoodsVisuals()


# In[5]:


e.avg_prices()


# In[ ]:




