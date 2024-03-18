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

#%%
#functions to convert into geojson
def hexagons_dataframe_to_geojson(df_hex, file_output = None, column_name = "value"):
    list_features = []
    for i,row in df_hex.iterrows():
        try:
            geometry_for_row = { "type" : "Polygon", "coordinates": [h3.h3_to_geo_boundary(h=row["hex_id"],geo_json=True)]}
            feature = Feature(geometry = geometry_for_row , id=row["hex_id"], properties = {column_name : row[column_name]})
            list_features.append(feature)
        except:
            print("An exception occurred for hex " + row["hex_id"]) 

    feat_collection = FeatureCollection(list_features)
    geojson_result = json.dumps(feat_collection)
    return geojson_result

#filtering function
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

    Bohemia=IBD[IBD['iid1'].isin(ids) | IBD['iid2'].isin(ids)]

    countriesiid1=[]
    countriesiid2=[]
    lat1=[]
    lat2=[]
    lon1=[]
    lon2=[]

    for x in Bohemia.index:
        try:
            z=names.loc[(names['Genetic ID'] == Bohemia["iid1"].iloc[x] )| (names['Master ID'] == Bohemia["iid1"].iloc[x])].values[0]
            countriesiid1.append(z[14].strip(" "))
            lat1.append(z[15])
            lon1.append(z[16])
            z=names.loc[(names['Genetic ID'] == Bohemia["iid2"].iloc[x]) | (names['Master ID'] == Bohemia["iid2"].iloc[x])].values[0]
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

    Hex=coordinates(Bohemia)
    return(Hex)

#fucntion to get the hexagons
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

#function to draw the map
def choropleth_map(df_aggreg, column_name = "value", border_color = None, fill_opacity = 0.7, color_map_name = "Reds", initial_map = None):
    name_layer = "Choropleth " + str(df_aggreg)
    
    if initial_map is None:
        initial_map = folium.Map(location= [47, 4], zoom_start=2.3, tiles="cartodbpositron")

    geojson_data = hexagons_dataframe_to_geojson(df_hex = df_aggreg, column_name = column_name)
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': '#800020',
            'color': border_color,
            'weight': 1,
            'fillOpacity': fill_opacity 
        }, 
        name = name_layer
    ).add_to(initial_map)

    app = Dash('MAP')

    app.layout = html.Div(dl.Map([dl.TileLayer(),dl.FeatureGroup([
    dl.Polygon(
            positions=h3.h3_to_geo_boundary(hexagon),
            color=None,
            fill=True,
            fillColor='#800020')
            for hexagon in df_aggreg['hex_id']])],
    center=[56,10], zoom=2.5, style={'height': '80vh'}))


    return(app)

#%% 
#Initial datasets
with open("ibd220.ibd.v54.1.pub.tsv", "r") as DataBase:
    samples=pd.read_csv(DataBase, sep= '\t')

nam=pd.read_excel("AADRAnnotation.xlsx")

#%% Running the fucntions
testHex=filtering(nam,samples,'Madrid, Humanejos')
app=choropleth_map(testHex, column_name = "length", border_color = None, fill_opacity = 0.05, color_map_name = "Reds", initial_map = None)

#%%
if __name__ == '__main__':
    app.run_server(debug=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#%%


# %%
