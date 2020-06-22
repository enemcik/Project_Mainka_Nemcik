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

PORT=8080

def user_prompter():
    print("\nWelcome to Erik's and Paul's project for JEM207@CharlesUni. Answer the following questions to get the appropriate output.")
    while True:
        txt = input('\nDo you already have downloaded data from the specified websites? [Y/N]')
        if txt not in ('Y', 'y', 'N', 'n'):
            print("\nNot an appropriate choice. Please input Y if you already have downloaded data and otherwise input N.")
        else:
            break
    if txt in ('Y','y'):
        while True:
            txt_a = input('\nDo you already have geocoded data? [Y/N]')
            if txt_a not in ('Y', 'y', 'N', 'n'):
                print("\nNot an appropriate choice. Please input Y if you already have geocoded data and otherwise input N.")
            else:
                break
        if txt_a in ('Y','y'):
            print('\nGreat! Here are your ready-to-go maps.\n')
            exec(open("3_Neighborhoods_data_prep.py").read(), globals())
            exec(open("4_Granular_map.py").read(),globals())
        elif txt_a in ('N','n'):
            print('\nLet me geocode the data for you. This might take several hours.')
            exec(open("2_Geocoding.py").read(), globals())             
            print('\nHere are your ready-to-go maps.')
            exec(open("3_Neighborhoods_data_prep.py").read(), globals())
            exec(open("4_Granular_map.py").read(),globals())
    elif txt  in ('N','n'):
        print('\nLet me fetch the required data for you. This might take several hours.')
        exec(open("1_Downloader.py").read(), globals())
        print('\nData downloaded. Geocoding...')
        exec(open("2_Geocoding.py").read(), globals())
        print('\nHere are your ready-to-go maps.')
        exec(open("3_Neighborhoods_data_prep.py").read(), globals())
        exec(open("4_Granular_map.py").read(),globals())
    while True:
        txt_b = input('\nDo you want to open the granular map now in your browser? [Y/N]')
        if txt_b not in ('Y', 'y', 'N', 'n'):
            print("\nNot an appropriate choice. Please input Y if you want to open the granular map now in your browser and otherwise input N.")
        else:
            break
    if txt_b in ('Y','y'):
            os.system("folium_map.html")
    else:
        pass
    while True:
        txt_c = input('\nDo you want to open the neighborhoods map now in your browser? [Y/N]')
        if txt_c not in ('Y', 'y', 'N', 'n'):
            print("\nNot an appropriate choice. Please input Y if you want to open the neighborhoods map now in your browser and otherwise input N.")
        else:
            break
    if txt_c in ('Y','y'):
            os.system(f"bokeh serve --show --port {PORT} 5_Neighborhoods_visuals.py")
    else:
        print('\nExiting programm now')

user_prompter()
