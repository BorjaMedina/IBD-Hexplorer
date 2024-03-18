#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 09:45:26 2024

@author: inf-47-2023

IBD PROJECT - BINP29 - BORJA MEDINA DE LAS HERAS
"""
#STEPS
# Im going o start with a zone, obtain a number and the do the map.
# If im able i wil try to expand to the rest of the zones.


#%% import libraries
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import csv
import re
import geopy
from geopy.geocoders import Nominatim
import countries
import kaleido
import plotly.express as px
import nbformat
import country_converter as coco

#%% open databases

with open("testingIBDData.tsv", "r") as DataBase:
    Bohemia=pd.read_csv(DataBase, sep= '\t')

names=pd.read_excel("AADRAnnotation.xlsx")


#%%
'''
for x in range(len(names['Political Entity'])):
    names['Political Entity'].replace(names['Political Entity'][x], names['Political Entity'][x].strip())

names['Political Entity'].replace('Russia', 'Russian Federation')
names['Political Entity'].replace('USA', 'United States of America')
names['Political Entity'].replace('Turkey', 'Türkiye')
names['Political Entity'].replace('Czech republic', 'Czechia')
'''
#%%
'''
import pycountry
input_countries = names['Political Entity']

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2
codes = [countries.get(country, 'Unknown code') for country in input_countries]
'''
#%%
'''
names['ISO']=codes
'''

#%% 
# Add the countries + latitudes and longitudes to the table
countriesiid1=[]
countriesiid2=[]
lat1=[]
lat2=[]
lon1=[]
lon2=[]

for x in range(len(Bohemia)):
    try:
        z=names.loc[(names['Genetic ID'] == Bohemia["iid1"][x] )| (names['Master ID'] == Bohemia["iid1"][x])].values[0]
        countriesiid1.append(z[14].strip(" "))
        lat1.append(z[15])
        lon1.append(z[16])
        z=names.loc[(names['Genetic ID'] == Bohemia["iid2"][x]) | (names['Master ID'] == Bohemia["iid2"][x])].values[0]
        countriesiid2.append(z[14].strip(" "))
        lat2.append(z[15])
        lon2.append(z[16])
    except IndexError:
        Bohemia.drop(x, inplace=True)
        pass

Bohemia["iid1Country"]=countriesiid1
Bohemia["iid2Country"]=countriesiid2
Bohemia["lat1"]=lat1
Bohemia["long1"]=lon1
Bohemia["lat2"]=lat2
Bohemia["long2"]=lon2

#%% 
# MODIFYING SOME COORDINATES
for o in Bohemia.index:
    if (Bohemia["lat2"][o]==".." or Bohemia["long2"][o]==".."):
        optLats=(Bohemia["lat2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()[(Bohemia["lat2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()!=".."]
        Bohemia["lat2"][o]=optLats[optLats.keys()[0]]
        optLats=(Bohemia["long2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()[(Bohemia["long2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()!=".."]
        Bohemia["long2"][o]=optLats[optLats.keys()[0]]
    if (Bohemia["lat1"][o]==".." or Bohemia["long1"][o]==".."):
        optLats=(Bohemia["lat2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid1Country"])).dropna()[(Bohemia["lat2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid1Country"])).dropna()!=".."]
        Bohemia["lat1"][o]=optLats[optLats.keys()[0]]
        optLats=(Bohemia["long2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid1Country"])).dropna()[(Bohemia["long2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid1Country"])).dropna()!=".."]
        Bohemia["long1"][o]=optLats[optLats.keys()[0]]

#%%
# OBTAIN THE ISO CODES USING LONGITUDE AND LATITUDE
loc1={}

for l in Bohemia.index:
    loc1[(",".join([str(Bohemia.loc[l][12]), str(Bohemia.loc[l][13])]))]=None
    loc1[(",".join([str(Bohemia.loc[l][14]), str(Bohemia.loc[l][15])]))]=None
loc1.pop('..,..',None)

for x in loc1.keys():
    locator = Nominatim(user_agent="my_geocoder", timeout=10)
    loc1[x]=((locator.reverse(x))).raw['address']['country_code'].upper()

#%%
Bohemia['ISO1']=np.nan
Bohemia['ISO2']=np.nan

for v in Bohemia.index:
    Bohemia['ISO1'][v]=loc1[(",".join([str(Bohemia.loc[v][12]), str(Bohemia.loc[v][13])]))]
    Bohemia['ISO2'][v]=loc1[(",".join([str(Bohemia.loc[v][14]), str(Bohemia.loc[v][15])]))]

#%% 
# Count the number of times it appears and sum the length per country
CountryPoints= dict.fromkeys((loc1.values()),0)
CountryCounts= dict.fromkeys((loc1.values()),0)

for z in Bohemia.index:
    if ((Bohemia["ISO1"][z]=="CZ") and (Bohemia["ISO2"][z]=="CZ")):
        CountryPoints["CZ"]= CountryPoints["CZ"] + Bohemia.loc[z]["length"]
        CountryCounts["CZ"]= CountryCounts["CZ"] + 1

    elif (Bohemia["ISO1"][z]=="CZ"):
        CountryPoints[Bohemia["ISO2"][z]]= CountryPoints[Bohemia["ISO2"][z]] + Bohemia.loc[z]["length"]
        CountryCounts[Bohemia["ISO2"][z]]= CountryCounts[Bohemia["ISO2"][z]] + 1
    elif (Bohemia["ISO2"][z]=="CZ"):
        CountryPoints[Bohemia["ISO1"][z]]= CountryPoints[Bohemia["ISO1"][z]] + Bohemia.loc[z]["length"]
        CountryCounts[Bohemia["ISO1"][z]]= CountryCounts[Bohemia["ISO1"][z]] + 1



#%%
#pd.DataFrame.from_dict(CountryPoints, orient='index').to_csv('CountryPoints.csv', index=True, header=False)
#pd.DataFrame.from_dict(CountryCounts,orient='index').to_csv('CountryCounts.csv', index=True, header=False)

#%%

'''
data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_with_codes.csv')

data.drop(['year','lifeExp', 'pop', 'gdpPercap'], axis=1, inplace=True)
data.drop_duplicates(inplace=True)
data["ISO2L"]=coco.convert(names= data["iso_alpha"], to="ISO2")
'''

#%%
'''len(set(sorted(data['country'])).intersection(np.unique(names['Political Entity'])))

result = [e for e in np.unique(names['Political Entity']) if e not in sorted(data['country'])]


#%%
for x in result:
    for z in sorted(data['country']):
        if fuzz.ratio(x,z)>60:
            #names['Political Entity'][np.where(names['Political Entity']==z)]=x
            print(z,x)

'''
#%%
'''
names['Political Entity'][np.where(names['Political Entity']=="Abkhazia")]="Georgia"
names['Political Entity'][np.where(names['Political Entity']=="Channel Islands")]="Guernsey"
names['Political Entity'][np.where(names['Political Entity']=="Crimea")]="Ukraine"
'''

#%%
befPoint={"ISO3":coco.convert(names= CountryCounts.keys(), to="ISO3"), "counts": CountryCounts.values()}
points=pd.DataFrame(befPoint)
#%%
fig = px.choropleth(points, locations="ISO3", color="counts", hover_name='ISO3', projection='Mercator', title='Counts')
#%%
fig.show()
#%%
fig.write_image("figure.png", engine="kaleido")


#%% DRAWING HEXAGONS
'''import matplotlib.pyplot as plt
from h3 import h3

def draw_hexagons(center_coordinates, resolution, num_hexagons):
    fig, ax = plt.subplots()
    
    for i in range(num_hexagons):
        hex_id = h3.geo_to_h3(center_coordinates[0], center_coordinates[1], resolution)
        vertices = h3.h3_to_geo_boundary(hex_id, geo_json=True)
        latitudes, longitudes = zip(*vertices)
        ax.plot(longitudes + (longitudes[0],), latitudes + (latitudes[0],), marker='o')

    ax.set_aspect('equal')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Hexagons')
    plt.grid(True)
    plt.show()

# Example usage:
center_coordinates = (37.7749, -122.4194)  # San Francisco coordinates
resolution = 9  # Hexagon resolution (0-15)
num_hexagons = 1  # Number of hexagons to draw

draw_hexagons(center_coordinates, resolution, num_hexagons)

'''
#%%
'''
for o in Bohemia.index:
    if (Bohemia["lat2"][o]==".." or Bohemia["long2"][o]==".."):
        optLats=(Bohemia["lat2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()[(Bohemia["lat2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()!=".."]
        Bohemia["lat2",o]=optLats[optLats.keys()[0]]
        optLats=(Bohemia["long2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()[(Bohemia["long2"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()!=".."]
        Bohemia["long2",o]=optLats[optLats.keys()[0]]
    if (Bohemia["lat1"][o]==".." or Bohemia["long1"][o]==".."):
        optLats=(Bohemia["lat1"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()[(Bohemia["lat1"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()!=".."]
        Bohemia["lat1",o]=optLats[optLats.keys()[0]]
        optLats=(Bohemia["long1"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()[(Bohemia["long1"].where(Bohemia["iid2Country"]==Bohemia.loc[o]["iid2Country"])).dropna()!=".."]
        Bohemia["long1",o]=optLats[optLats.keys()[0]]
'''



#%%
