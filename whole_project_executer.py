#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
This script will execute the 5 distinct parts of our Prague rental prices visualisation in the correct order. However, we do not 
recommend to only do this. The reason is that you will not be able to understand what is actually going on in the single scripts, 
you need a couple of packages installed to execute all the scripts, some of which might have conflicts with one another, and finally 
the process will probably take a couple of hours to execute everything. We therefore recommend to rather execute each script by itself, as
they are all self sufficient in the sense that they save a file in your working directory which then can be processed by the following script.
'''


# In[ ]:


exec(open("Bez_Real_Downloader.py").read())


# In[ ]:


exec(open("Geocoding.py").read())


# In[ ]:


exec(open("Folium_map.py").read())


# In[ ]:


exec(open("Neighborhoods_data_prep.py").read())


# In[ ]:


exec(open("Neighborhoods_visuals.py").read())

