#Visualize ancient IBD connections on a map
#Borja Medina de las Heras



#%%
#some necessary libraries
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_leaflet as dl
from dash.dependencies import Input, Output
import h3
import folium
from geojson import Feature, Point, FeatureCollection
import json
import matplotlib.pyplot as plt
import numpy as np
import sys

#%%
#functions to draw hexagons

def filtering(names, IBD, population):
    for o in names.index:
        if (names["Lat."][o]==".." or names["Long."][o]==".."):
            names.drop(o, inplace=True)

    hex_id=[]
    for i in names.index:
        h3_index = h3.geo_to_h3(float(names['Lat.'][i]), float(names['Long.'][i]),resolution=3)
        hex_id.append(h3_index)
    names['hex_id']=hex_id

    hex= names['hex_id'][names.index[names['Locality']==population][0]]
    ids= names['Master ID'][names.index[names['hex_id']==hex]]

    Bohemia=IBD[IBD['iid1'].isin(ids) | IBD['iid2'].isin(ids)].reset_index()

    countriesiid1=['error']*len(Bohemia['iid1'])
    countriesiid2=['error']*len(Bohemia['iid1'])
    lat1=['error']*len(Bohemia['iid1'])
    lat2=['error']*len(Bohemia['iid1'])
    lon1=['error']*len(Bohemia['iid1'])
    lon2=['error']*len(Bohemia['iid1'])

    errors=[]
    for x in range(len(Bohemia['iid1'])):
        try:
            z=names.loc[(names['Genetic ID'] == Bohemia["iid1"].iloc[x] )| (names['Master ID'] == Bohemia["iid1"].iloc[x])].values[0]
            countriesiid1[x]=z[14].strip(" ")
            lat1[x]=z[15]
            lon1[x]=z[16]
            z=names.loc[(names['Genetic ID'] == Bohemia["iid2"].iloc[x]) | (names['Master ID'] == Bohemia["iid2"].iloc[x])].values[0]
            countriesiid2[x]=z[14].strip(" ")
            lat2[x]=z[15]
            lon2[x]=z[16]
        except IndexError:
            Bohemia.drop(x, inplace=True)
            countriesiid1[x]='error'
            countriesiid2[x]='error'
            lat1[x]='error'
            lon1[x]='error'
            lat2[x]='error'
            lon2[x]='error'
            pass

    while 'error' in lat1:
        countriesiid1.remove('error')
        countriesiid2.remove('error')
        lat1.remove('error')
        lon1.remove('error')
        lat2.remove('error')
        lon2.remove('error')

    Bohemia["iid1Country"]=countriesiid1
    Bohemia["iid2Country"]=countriesiid2
    Bohemia["lat1"]=lat1
    Bohemia["long1"]=lon1
    Bohemia["lat2"]=lat2
    Bohemia["long2"]=lon2

    allHex=coordinates(Bohemia)
    return(allHex,hex)

def coordinates(dataset):
    Hex1= dataset[["iid1","lat1","long1"]].copy()
    Hex1=Hex1.rename(columns={'iid1': 'iid','lat1': 'latitude', 'long1': 'longitude'})
    Hex2= dataset[["iid2","lat2","long2"]].copy()
    Hex2=Hex2.rename(columns={'iid2': 'iid','lat2': 'latitude', 'long2': 'longitude'})

    Hex=pd.concat([Hex1,Hex2])

    for o in Hex.index:
        if (Hex["latitude"].iloc[o]==".." or Hex["longitude"].iloc[o]==".."):
            Hex.drop(o, inplace=True)

    hex_id=[]
    for i in Hex.index:
        h3_index = h3.geo_to_h3(float(Hex['latitude'].iloc[i]), float(Hex['longitude'].iloc[i]),resolution=3)
        hex_id.append(h3_index)
    Hex['hex_id']=hex_id
    return(Hex)


def choropleth_map(df_aggreg,originHex, names, border_color = None, fill_opacity = 0.05, color_map_name = "Reds", initial_map = None):
    app = Dash('MAP')
    app.layout = html.Div(dl.Map([dl.TileLayer(),dl.FeatureGroup([
    dl.Polygon(
            positions=h3.h3_to_geo_boundary(hexagon),
            color=None,
            fill=True,
            fillColor='#800020')
            for hexagon in df_aggreg['hex_id']]),
            dl.FeatureGroup([
    dl.Polygon(
            positions=h3.h3_to_geo_boundary(originHex),
            color="Green",
            fill=False
        )]
    )],
    center=[56,10], zoom=2.5, style={'height': '80vh'}))

    app2=Dash('Dropdown')
    app2.layout = html.Div([
    dcc.Dropdown(
        id='Locality',
        options= [{'label': name, 'value': name} for name in np.unique(names)]  # Default value
    ),
    html.Div(id='map-container')])

    app3=Dash('Combined')
    combined_layout = html.Div([
        html.Div([app.layout], style={'width': '100%','height': '90px', 'display': 'inline-block'}),
        html.Div([app2.layout], style={'width': '100%','height': '10px' , 'display': 'inline-block'})])
    app3.layout=combined_layout

    '''
    @app.callback(
        Output('population', 'value'),
        Input('Locality', 'value'))
    '''

    return(app,app2,app3)

#%% 
#Initial datasets
with open("ibd220.ibd.v54.1.pub.tsv", "r") as DataBase:
    samples=pd.read_csv(DataBase, sep= '\t')

nam=pd.read_excel("AADRAnnotation.xlsx")

#%%
class NumberOfFilesError(Exception):
    pass
try:
    if len(sys.argv) == 2:
        pop=sys.argv[1]
        print(pop)
    elif len(sys.argv) == 1:
        pop="Madrid, Humanejos"
        print("You have not specified a name for a population. The population used will be Madrid, Humanejos")
    else:
        raise NumberOfFilesError

except NumberOfFilesError:
    print("Re-run the program with the correct number and the correct names of the files")
    exit()


#%%
allhex,origin=filtering(nam,samples,pop)

#%%
app,app2,combined=choropleth_map(allhex,origin, nam['Locality'], border_color = None, fill_opacity = 0.001, color_map_name = "Reds", initial_map = None)

#%%
if __name__ == '__main__':
    combined.run_server(debug=True, port=8051)
    #app2.run_server(debug=True, port=8051)
    #app.run_server(debug=True, port=8050)

# %%
