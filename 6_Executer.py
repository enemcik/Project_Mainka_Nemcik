'''
This script will execute the 5 distinct parts of our Prague rental prices visualisation in the correct order. However, we do not 
recommend to only do this. The reason is that you will not be able to understand what is actually going on in the single scripts, 
you need a couple of packages installed to execute all the scripts, some of which might have conflicts with one another, and finally 
the process will probably take a couple of hours to execute everything. We therefore recommend to rather execute each script by itself, as
they are all self sufficient in the sense that they save a file in your working directory which then can be processed by the following script.

We have created a function that will guide the user via terminal commands through the visualisation process.
'''
#visualisation
import folium
import folium.plugins as plugins
from folium.plugins import MarkerCluster
#from ipywidgets import interact
import requests
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import pandas as pd
import numpy as np
import re
import json
from gensim.utils import deaccent
import random
import os
import math
#geocoding
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.palettes import brewer
from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select
from bokeh.layouts import widgetbox, row, column
import geopy
import geopandas as gpd
from geopy.extra.rate_limiter import RateLimiter

def user_prompter():
    print("Welcome to Erik's and Paul's project for JEM207@CharlesUni. Answer the following questions to get the appropriate output.")
    txt = input('Do you already have downloaded data from the specified websites? [Y/N]')
    if txt == 'Y' or 'y':
        txt_a = input('Do you already have geocoded data? [Y/N]')
        if txt_a == 'Y' or 'y':
            print('Great! Here are your ready-to-go maps.')
            exec(open("3_Neighborhoods_data_prep.py").read(), globals())
            exec(open("4_Granular_map.py").read(),globals())
            print('\n')
            exec(open("5_Neighborhoods_visuals.py").read(), globals())
        elif txt_a == 'N' or 'n':
            print('Let me geocode the data for you. This might take several hours.')
            exec(open("2_Geocoding.py").read(), globals())
                
            print('Here are your ready-to-go maps.')
            exec(open("3_Neighborhoods_data_prep.py").read(), globals())
            exec(open("4_Granular_map.py").read(),globals())
            print('\n')
            exec(open("5_Neighborhoods_visuals.py").read(),globals())
        else:
            print('Wrong input!')
    elif txt == 'N' or 'n':
        print('Let me fetch the required data for you. This might take several hours.')
        exec(open("1_Downloader.py").read(), globals())
        print('Data downloaded. Geocoding...')
        exec(open("2_Geocoding.py").read(), globals())
        print('Here are your ready-to-go maps.')
        exec(open("3_Neighborhoods_data_prep.py").read(), globals())
        exec(open("4_Granular_map.py").read(),globals())
        print('\n')
        exec(open("5_Neighborhoods_visuals.py").read(),globals()) 
    else:
        print('Wrong input!')

user_prompter()


