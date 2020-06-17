#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import folium
import folium.plugins as plugins
from folium.plugins import MarkerCluster
from tqdm import tqdm


# In[2]:


fileDir = os.path.dirname(os.path.realpath('__file__'))


# In[3]:


def FoliumMap(df_):
    '''
    Function creates a new, empty map with folium, the map doesnt contain any datapoints yet but is intialized at the mean latitude & longitude
    point in our dataset. Then adds data points = flats (markers) to the map. For each observation (=row) of the dataset we read the latitude & longitude
    to create an icon which will be a display for the flat on the map. Furthermore we add a pop up text with basic information about the flat
    to each icon. We create clusters to achieve better visualisation.
    '''
    new_map = folium.Map(location=[df_['latitude'].mean(), df_['longitude'].mean()], 
                        zoom_start=12,
                        tiles='cartodbpositron')
    mc = MarkerCluster()# create empty cluster object
    for row in tqdm(df_.itertuples()):
     mc.add_child(folium.Marker(location=[row.latitude, row.longitude], #create markers and add to cluster
         popup= folium.Popup(
             folium.IFrame(
                 ('''Size: {Size} <br>
                  m2: {m2} <br>
                  Base Price: {bp} <br>
                  Utilities: {up} <br> 
                  Total Price: {TotalPrice}'''
                  ).format(Size=row.Size, m2=row.m2, bp=row[5], up=row[6], TotalPrice=row[7]),
                  width=200, height=100)),
         icon=folium.Icon(icon='home'))) #define icon symbol
    new_map.add_child(mc) 
    new_map.save(outfile='folium_map.html') #saves file as html file in working directory
    return new_map

dataframe = pd.read_pickle(fileDir + '\\Data\\' +'geo_df.pkl') #load from here

FoliumMap(dataframe)


# In[ ]:




