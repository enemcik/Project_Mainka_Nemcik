#!/usr/bin/env python
# coding: utf-8

# In[22]:


import os
import pandas as pd
import json

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


# In[23]:


fileDir = os.path.dirname(os.path.realpath('__file__'))


# In[24]:


# This dictionary contains the formatting for the data in the plots, which will be used in the interactive neighborhood map
format_data = [('Price', 10000, 25000,'0,0', 'Price'),
              ('Median_price', 10000, 25000,'0,0', 'Median Price'),
              ('Avg_m2_price', 180, 350,'0,0', 'Price per Square Metre')] #more options to be added later
 
#Create a DataFrame object from the dictionary 
format_df = pd.DataFrame(format_data, columns = ['field' , 'min_range', 'max_range' , 'format', 'verbage'])

# Add Bokeh hover tool, which will be used in the interactive neighborhood map - allows the user to hover over an item and display values.
hover = HoverTool(tooltips = [ ('Neighborhood','@NAZEV_MC'),
                               ('Average Price', '@Price'),
                               ('Median Price', '@Median_price'),
                               ('Average m2', '@m2'),
                               ('Crown per m2', '@Avg_m2_price'),
                               ('Number of Apartments', '@Number_of_Apartments')])


# In[25]:


# Create a plotting function
def make_plot(field_name, color='Reds'):
        '''
        Creates an interactive Choropleth map represents statistical data through various shading patterns for the (Prague) neighbourhoods according to the prices.
        The interactive map allows the user to select the data they prefer to view.
        '''
        # Set the format of the colorbar
        min_range = format_df.loc[format_df['field'] == field_name, 'min_range'].iloc[0]
        max_range = format_df.loc[format_df['field'] == field_name, 'max_range'].iloc[0]
        field_format = format_df.loc[format_df['field'] == field_name, 'format'].iloc[0]

        palette = brewer[color][8] #Define a sequential multi-hue color palette        
        palette = palette[::-1] # Reverse color order so that dark red is highest obesity.
        color_mapper = LinearColorMapper(palette = palette, low = min_range, high = max_range) # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
        # Create color bar.
        format_tick = NumeralTickFormatter(format=field_format)
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=18, formatter=format_tick,
        border_line_color=None, location = (0, 0))
        # Create figure object.
        verbage = format_df.loc[format_df['field'] == field_name, 'verbage'].iloc[0]
        p = figure(title = 'Apartment Rental ' + verbage + ' by City Parts in Prague', 
                    plot_height = 650, plot_width = 850,
                    toolbar_location = None)
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.axis.visible = False
        
        p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper}, # Add patch renderer to figure. 
                  line_color = 'black', line_width = 0.25, fill_alpha = 1)
        p.add_layout(color_bar, 'right') # Specify color bar layout.
        p.add_tools(hover)  # Add the hover tool to the graph

        return p


# In[26]:


def update_plot(attr, old, new):
    '''
    Callback function for make_plot(): Important for widget tools from Bokeh: Users when map is on the Web can select a criteria they want to have displayed
    (for us the options are: 'Price', 'Median Price' or 'Price per Square Metre'). Bokeh calls when the .on_change method is used 
    (when a change is made using the widget) the update_plot function. update_plot is a callback function with three parameters:
    the attr parameter is simply the ‘value’ passed (select.value = criteria), the old and new are internal parameters used by Bokeh.
    '''
    new_data = json_data
    cr = select.value # The input cr is the criteria selected from the select box
    input_field = format_df.loc[format_df['verbage'] == cr, 'field'].iloc[0]
    p = make_plot(input_field) # Update the plot based on the changed inputs
    layout = column(p, widgetbox(select))  # Update the layout, clear the old document and display the new document
    curdoc().clear()
    curdoc().add_root(layout)
    geosource.geojson = new_data # Update the data

    
    


# In[27]:


'''Certain elements, like data, input_field (slection object) have to be defined outside of the make_plot function otherwise the update_plot function does not work.'''

with open(fileDir + '\\Data\\merged_visuals_data.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
# 
geosource = GeoJSONDataSource(geojson = json_data)

input_field = 'Median_price'

# Call the plotting function
p = make_plot(input_field)

# Make a selection object from which users can choose: select
select = Select(title='Select Criteria:', value='Price', options=['Price', 'Median Price',
                                                                               'Price per Square Metre'])
select.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p, widgetbox(select))

curdoc().add_root(layout)
# Display the current document
output_notebook()
show(p)

#bokeh serve --show Downloader.ipynb -in anaconda prompt shows interactive map in local server 


# In[ ]:




