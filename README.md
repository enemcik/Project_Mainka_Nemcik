# Project of Erik Nemcik & Paul Mainka

## For Charles University of Prague, Faculty of Social Sciences - Data Processing in Python (JEM207)

### Data source: bezrealitky.cz & reality.idnes.cz 
Disclaimer: We have used the data processed by us exclusively for academic purposes and have  not received any monetary gain from it. Furthermore, the data represents only a snapshot of the rental situation in Prague, that is, at the time we scraped it (June 2020).

### Procedure: 
1. As a first step we scraped the data from bezrealitky.cz & reality.idnes.cz and stored it. This action is performed by the "1_Downloader.py" script. This step may take some time (~30-90 min).

2. We merge and process the data and then add geographic addresses (latitude and longitude) using geocoding (via the Nomatim API). This step is performed by the "2_Geocoding.py" script. This step can take a few hours (~2-4h).

3. We preprocess our data for visualisation and save the prepared data set. This is done by the "3_Neighborhoods_data_prep.py" script.

4. We visualize our data creating a granular map by using folium maps, on which each apartment is displayed on an interactive map of Prague. This is carried out by the "4_Granular_Map.py" script.

5. An interactive map is being created in which differences in average, median and average square metre prices for the different neighbourhoods in Prague are illustrated by colour variations. The "5_Neighborhoods_visuals.py" script performs this action.

#### Additional files and information:
- To execute all the scripts you will need multiple packages. Most importantly geopandas, which might cause problems with some other dependencies. Therefore, we recommend, in case you don't have geopandas yet, to create a new environment and install all the required packages for this project there. 

- Furthermore, the "Downloader.ipynb" is a Jupyter notebook file which contains all the five scripts descript above. Note however, that the "Downloader.ipynb" is not completly up-to-date compared to the .py files (although the differences are marginal, mostly contains less descriptive docstrings and the code is not as pretty prepared as in the .py files).

- The "6_Executer.py" file is an executable script which will execute the 5 distinct parts of our Prague rental prices visualisation in the correct order. However, we do not recommend to only do this. The reason is that you will not be able to understand what is actually going on in the single scripts, you need a couple of packages installed to execute all the scripts and finally the process will probably take a couple of hours to execute everything. We therefore recommend to rather execute each script by itself, as they are all self sufficient in the sense that they save a file in your working directory which then can be processed by the following script.

- The files in the data file are containing the outputs of the distinct scripts, therefore it is possible to execute the scripts in different order as described above, utilizing the provided data. Note however, that this data is based on a scrape on the 17.06.2020 and it will not be automatically updated, therefore you would be working with outdated data.



