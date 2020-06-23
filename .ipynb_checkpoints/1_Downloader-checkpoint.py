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
import platform


fileDir = os.path.dirname(os.path.realpath('__file__'))
'''Create a new Folder "Data" in the current working directory to store & access the data files which will be produced throughout this script'''
newfolder = r'Data' 
if not os.path.exists(newfolder): #if already exists will not be created again
    os.makedirs(newfolder)


### Establishing functions

def get_soups(links, name):
       '''
       This function iterates over all search pages, converts them into a BeautifulSoup object and stores them in a JSON file as 
       outside of this script. The keys of the dictoniary distinguish here between the different objects/HTML-pages. 
       '''
       count = 0
       dict_ = {}
       soups = []
       for link in tqdm(links):
           sleep(random.uniform(0.5, 2))
           request = requests.get(link)
           request.encoding='UTF-8'
           soups.append(BeautifulSoup(request.text,'lxml'))
       for soup in soups:
           dict_[count] = str(deaccent(soup).encode("utf-8"))
           count += 1
       with open(name, 'w') as write_file:
           json.dump(dict_, write_file, indent = 4)


### Downloading

class DownloaderBezRealitky(): 
    def __init__(self):
        '''
        For the bezrealitky search, you need to iterate over search pages. Self.page_bezrealitky stores the maximum amount
        of pages and then via self.link a list of all pages from search is created in self.hrefs_bezrealitky.
        '''
        self.link = 'https://www.bezrealitky.cz/vypis/nabidka-pronajem/byt/praha?_token=pr1lf-vKwDFfmFbICiz2PfC-Zdwq-2JolXi4MeMHsrw&page=1'
        self.request = requests.get(self.link)
        self.request.encoding='UTF-8'
        self.soup = BeautifulSoup(self.request.text,'lxml')
        self.page_bezrealitky = int(self.soup.findAll('a',{'class':'page-link pagination__page'})[-2].text)
        self.hrefs_bezrealitky = ['https://www.bezrealitky.cz/vypis/nabidka-pronajem/byt/praha?_token=pr1lf-vKwDFfmFbICiz2PfC-Zdwq-2JolXi4MeMHsrw&page=' 
                                  + str(i) for i in range(1,self.page_bezrealitky)]
        self.soups = []
        self.counter = 0 #counter

    def get_data(self):
        '''
        Main method to obtain and transform the data. HTMLs are read from the JSON file and stored in a list (soup_list) 
        within this script. Next, the method iterates over the list, converts the strings in the list into a BeautifulSoup
        object and parses the html for relevant data. At the end, a nested dictionary (dicts) is created and stored
        as a json file outside of this script.
        '''
        if platform.system() == 'Darwin':
            with open(fileDir + '/Data/bezrealitky_links.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
        else:
            with open(fileDir + '\\Data\\bezrealitky_links.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
        soup_list = list(content.values())
        dicts = {}
        counter = 0
        for soup in tqdm(soup_list):
            descrips = [] #empty list for apartment values
            values = [] #empty list for apartment prices
            vals = BeautifulSoup(soup,'lxml').findAll('strong', {'class':'product__value'}) #parsing for apartment values
            ##vals = soup.findAll('strong', {'class':'product__value'})
            for vl in vals:
                values.append(vl.text.strip())
            #img = soup.findAll('img')
            img = BeautifulSoup(soup,'lxml').findAll('img') #parsing for apartment info (street, city, size..)
            for i in img:
                if 'Pronajem' and 'obr. c. 1' in i['alt']: #info present at all pictures, let's take info from the first one
                        info = i['alt'].split(',')[0:4] #info separated by comma, split into a list
                        if 'Praha' == info[-1].strip(): #if street non present, insert a NaN instead
                            info.insert(2, 'NaN')
                            del info[-1]
                            m = info[1].split(' ')
                            info[1] = m[1]
                            descrips.append(info)
                        else:
                            m = info[1].split(' ')
                            info[1] = m[1]
                            descrips.append(info)
            count = 0
            for pp in values: #append apartment prices to info about apartments in list descrips
                try:
                    descrips[count].append(pp)
                    descrips[count][0] = descrips[count][0][-4:].strip()
                    count += 1
                except IndexError:
                    count += 1
                    continue
            for item in descrips:
                try:
                    if '+' in item[4]: #prices often written as '19000 Kč + 4000Kč' so we need to split it
                        prices = item.pop(4).split('+')
                        item.append(re.sub("[^0-9]", "", prices[0])) #keep only numeric characters, i.e. price
                        item.append(re.sub("[^0-9]", "", prices[1]))
                    else:
                        prices = [item.pop(4), '0'] #if only '19000 Kč', insert 0 as price for utilities not specified
                        item.append(re.sub("[^0-9]", "", prices[0]))
                        item.append(re.sub("[^0-9]", "", prices[1]))
                except IndexError:
                    continue
            for item in descrips: #store apartment info, price into a dictionary and index by counter
                try:
                    dict = {}
                    dict['Size'] = item[0]
                    dict['m2'] = re.sub("[^0-9]", "", item[1]) #keep only size, i.e. numeric characters
                    dict['Street'] = deaccent(item[2]) #deaccent to provent potential errors
                    dict['District'] = deaccent(item[3])
                    dict['Base Price'] = int(item[4])
                    dict['Utilities Price'] = int(item[5])
                    dict['Total Price'] = int(item[4]) + int(item[5])
                    dict['Source'] = 'bezrealitky.cz'
                    dicts[self.counter] = dict
                    self.counter += 1
                except IndexError:
                    #counter +=1
                    continue
        if platform.system() == 'Darwin':
            with open(fileDir + '/Data/bezrealitky.json', 'w') as write_file: #store data into a json file
                json.dump(dicts, write_file, indent = 4)
        else:
            with open(fileDir + '\\Data\\bezrealitky.json', 'w') as write_file: #store data into a json file
                json.dump(dicts, write_file, indent = 4)
                
a = DownloaderBezRealitky()

#for MAC/PC users
if platform.system() == 'Darwin':
    get_soups(a.hrefs_bezrealitky, fileDir + '/Data/bezrealitky_links.json')
else:
    get_soups(a.hrefs_bezrealitky, fileDir + '\\Data\\bezrealitky_links.json') 

a.get_data()

class DownloaderReality():
    def __init__(self):
        '''
        For the reality search, you need to iterate over search pages. Self.page_reality stores the maximum amount
        of pages and then via self.link a list of all pages from search is created in self.hrefs_reality.
        '''
        self.link = 'https://reality.idnes.cz/s/pronajem/byty/praha/?page=1'
        self.request = requests.get(self.link)
        self.request.encoding='UTF-8'
        self.soup = BeautifulSoup(self.request.text,'lxml')
        self.page_reality = int(self.soup.findAll('a',{'class':'btn btn--border paging__item'})[-1].text) - 1
        self.hrefs_reality = ['https://reality.idnes.cz/s/pronajem/byty/praha/?page=' 
                                  + str(i) for i in range(1,self.page_reality)]
        self.soups = []
        self.counter = 1000000 #counter - high number here to ensure that they get unique keys (ergo different from bezrealitky if that was executed first)
        
    def get_data(self):
        '''
        Main method to obtain and transform the data. HTMLs are read from the JSON file and stored in a list (soup_list) 
        within this script. Next, the method iterates over the list, converts the strings in txt file into a BeautifulSoup
        object and parses the html for relevant data. At the end, a nested dictionary (dicts) is created and stored
        as a json file outside of this script.
        '''
        if platform.system() == 'Darwin':
            with open(fileDir + '/Data/reality_idnes_links.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
        else:
            with open(fileDir + '\\Data\\reality_idnes_links.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
        soup_list = list(content.values())
        dicts = {}
        counter = 0
        for soup in tqdm(soup_list):
            descrips = [] #empty list for apartment values
            values = [] #empty list for apartment prices
            info_size = []
            apartments = []
            vals = BeautifulSoup(soup,'lxml').findAll('p', {'class':'c-list-products__price'}) #parsing for apartment values
            for vl in vals: #adding values
                values.append(re.sub("[^0-9]", "",vl.find('strong').text))
                
            locs = BeautifulSoup(soup,'lxml').findAll('p', {'class':'c-list-products__info'})
            for i in locs: #adding location
                if 'Komercni sdeleni' in i.text:
                    continue
                else:
                    temp_info = str(i.text)
                    temp_info = re.sub(r'^(?:\\n)+','', temp_info).strip()[:-2]
                    temp_info = temp_info.strip().split(',')
                    temp_info = [i.strip() for i in temp_info]
                    if len(temp_info) == 1:
                        temp_info.append(temp_info[0])
                        temp_info[0] = 'NaN'
                    if len(temp_info) == 3:
                        del temp_info[2]
                    descrips.append(temp_info)
                    
            sizes = BeautifulSoup(soup,'lxml').findAll('h2', {'class':'c-list-products__title'})
            for s in sizes: #adding size and m2
                try:
                    item = s.text.split('bytu')[1].strip()[:-2]
                    temp = item.split(',')
                    temp[1] = temp[1][:-10].strip()
                    info_size.append(temp)
                except IndexError:
                    continue
            
            for apart in range(0,len(info_size)):
                apartments.append(info_size[apart] + descrips[apart] + [values[apart]])
                
            for item in apartments: #store apartment info, price into a dictionary and index by counter
                try:
                    dict = {}
                    dict['Size'] = item[0]
                    dict['m2'] = item[1]
                    dict['Street'] = deaccent(item[2]) #deaccent to provent potential errors
                    dict['District'] = deaccent(item[3])
                    dict['Base Price'] = int(item[4])
                    dict['Utilities Price'] = 0
                    dict['Total Price'] = int(item[4])
                    dict['Source'] = 'reality.idnes.cz'
                    dicts[self.counter] = dict
                    self.counter +=1
                except ValueError:
                    #counter += 1
                    continue
        if platform.system() == 'Darwin':
            with open(fileDir + '/Data/idnes_reality.json', 'w') as write_file: #store data into a json file
                json.dump(dicts, write_file, indent = 4)
        else:
            with open(fileDir + '\\Data\\idnes_reality.json', 'w') as write_file: #store data into a json file
                json.dump(dicts, write_file, indent = 4)

b = DownloaderReality()

#for MAC/PC users
if platform.system() == 'Darwin':
    get_soups(b.hrefs_reality, fileDir + '/Data/reality_idnes_links.json')
else:
    get_soups(b.hrefs_reality, fileDir + '\\Data\\reality_idnes_links.json')

b.get_data()




