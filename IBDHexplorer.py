#importing some packages and fucntions
import dash
from dash.dependencies import Input, Output
import folium
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_leaflet as dl
import h3
from geojson import Feature, Point, FeatureCollection
import json
import matplotlib.pyplot as plt
import numpy as np
import sys

#define some fucntions necessary to create the maps
def filtering(names, IBD, population, hexagon, length):

    #some initial filtering
    #first we delete all the rows which coordiantes values are ..
    mask=(names["Lat."]!="..") & (names["Long."]!="..")
    names=names[mask]   

    #we filter by the length specified by the user
    mask= (IBD['length']>= length[0]) & (IBD['length']<= length[1])
    IBD=IBD[mask]

    #we get the hexagons using the resolution selected by the user (in this version of the app its going to be the same size for selecting a poopulation and for creating the map)
    hex_id=[]
    for i in names.index:
        h3_index = h3.geo_to_h3(float(names['Lat.'][i]), float(names['Long.'][i]),resolution=hexagon)
        hex_id.append(h3_index)
    names['hex_id']=hex_id

    #we are going to filter by population
    hex= names['hex_id'][names.index[names['Locality']==population][0]] #we get the hex id of the popualtion we are interested in
    ids1= names['Master ID'][names.index[names['hex_id']==hex]] # we get the Genetic ID and the Master ID because we have seen that sometimes in the IBD database they use one or another.
    ids2= names['Genetic ID'][names.index[names['hex_id']==hex]]
    ids=set(ids1)|set(ids2)
    Bohemia=IBD[IBD['iid1'].isin(ids) | IBD['iid2'].isin(ids)] #if either one of the the two ids involved in the IBD segemnts is present in the ids selection, maintain the row.

    names['Lat.']=names['Lat.'].astype(str)
    names['Long.']=names['Long.'].astype(str)
    names['coordinates']= names[['Lat.', 'Long.']].agg(','.join, axis=1)
    #we are going to create a dictionary witht the IDs and the coordinates to copy them into the new database.
    #the reason to create the dictionary is that it was the fastest way of handling so many lines.
    row_dict={}
    for index, row in names.iterrows():
        row_dict [row['Genetic ID']]= row['coordinates']
        row_dict [row['Master ID']]= row['coordinates']

    #we have filtered wso at least one f the ids is in the id list of the popualtion. But the other id might not even be in the list of the ADDR
    #we have to handle those errors
    lat1=['error']*len(Bohemia['iid1'])
    lat2=['error']*len(Bohemia['iid1'])
    lon1=['error']*len(Bohemia['iid1'])
    lon2=['error']*len(Bohemia['iid1'])

    #we try to append the coordiantes if its not possible because the id doesn't exist, we subsittute the line with "error"
    for x in range(0,len(Bohemia['iid1'])):
        try:
            lat1[x]=row_dict[Bohemia["iid1"].iloc[x]].split(',')[0]
            lon1[x]=row_dict[Bohemia["iid1"].iloc[x]].split(',')[1]
            lat2[x]=row_dict[Bohemia["iid2"].iloc[x]].split(',')[0]
            lon2[x]=row_dict[Bohemia["iid2"].iloc[x]].split(',')[1]
        
        except KeyError:
            Bohemia.iloc[x]=['error']*len(Bohemia.iloc[x])
            lat1[x]='error'
            lon1[x]='error'
            lat2[x]='error'
            lon2[x]='error'
            pass

    #we delete all thhe "errors" from the dataset and from the lists
    mask = Bohemia.apply(lambda row: 'error' in row.values, axis=1)
    Bohemia = Bohemia[~mask]

    while 'error' in lat1:
        lat1.remove('error')
        lon1.remove('error')
        lat2.remove('error')
        lon2.remove('error')

    #now that everything has the same length we join the datset with the lists
    Bohemia["lat1"]=lat1
    Bohemia["long1"]=lon1
    Bohemia["lat2"]=lat2
    Bohemia["long2"]=lon2

    #we rest the indexing, because right now there are a lot of indexes missing
    Bohemia=Bohemia.reset_index()
    #we return the dataset
    return(Bohemia,hex)

# this function is going to be used to get the coordinates of the hexagons represented in the map
# we have already calculated all the possible hexagons, so we could just copy it, 
# but his function would give us the chance in the future to make changes in the code so the resolution of the original population is differetn to the resolution of the popualtions painted in the map.
# We would juts need another input and change the size value of this function. Its an easy modeification. 
def coordinates(dataset,size):
    # we create a dataframe with all the ids and coordinates(its all we need to paint them)
    Hex1= dataset[["iid1","lat1","long1"]].copy()
    Hex1=Hex1.rename(columns={'iid1': 'iid','lat1': 'latitude', 'long1': 'longitude'})
    Hex2= dataset[["iid2","lat2","long2"]].copy()
    Hex2=Hex2.rename(columns={'iid2': 'iid','lat2': 'latitude', 'long2': 'longitude'})

    Hex=pd.concat([Hex1,Hex2])

    # we filter again for the (..) missing values although it shouldnt be necessary, we have already got rid of them
    for o in Hex.index:
        if (Hex["latitude"].iloc[o]==".." or Hex["longitude"].iloc[o]==".."):
            Hex.drop(o, inplace=True)

    #we calculte the hexagons ids and append them to the dataframe (Hex).
    hex_id=[]
    for i in Hex.index:
        h3_index = h3.geo_to_h3(float(Hex['latitude'].iloc[i]), float(Hex['longitude'].iloc[i]),resolution=size)
        hex_id.append(h3_index)
    Hex['hex_id']=hex_id
    return(Hex)

#fnction to get the layout of the map
def choropleth_map(df_aggreg,originHex, names, border_color = None, fill_opacity = 0.05, color_map_name = "Reds", initial_map = None):
    layout2 = html.Div([        
            html.Div([dl.Map([dl.TileLayer(),dl.FeatureGroup([
                dl.Polygon( #we paint all the red hexagons (related populations)
                        positions=h3.h3_to_geo_boundary(hexagon),
                        color=None,
                        fill=True,
                        fillColor='#800020',
                        fillOpacity= fill_opacity)
                        for hexagon in df_aggreg['hex_id']]), 
                        dl.FeatureGroup([
                dl.Polygon( #we paint the hexagon border in green of the selected population - location selected 
                        positions=h3.h3_to_geo_boundary(originHex),
                        color="Green",
                        fill=False
        )]
    )],
    center=[56,10], zoom=2.5, style={'height': '80vh'})],
    style={'width': '100%', 'height':'85%', 'display': 'inline-block'}),
    html.Div(id='windowIn')])

    return(layout2)

# function to create the first layout and to update everytime the filters are changed
def itself():
    #select the localities present on the IBD file to be able to put it on the dropdown
    totalids=np.unique(list(samples['iid1'])+list(samples['iid2']))
    localities = np.unique(nam['Locality'][nam['Genetic ID'].isin(totalids)])

    # Initialize the Dash app
    app = dash.Dash(__name__,suppress_callback_exceptions=True)
    # Define the layout for the first window
    layout1 = html.Div([
        #first we include our logo in the webpage (and the anme of our app)
        html.Img(src='https://www.dropbox.com/scl/fi/m9cmuqsgzxyjutdszbtzg/logoRojotop.png?rlkey=607jze6qiml76swqvhzt9j1nk&raw=1', style={'width': '370px', 'height': '100px', 'margin-top':'10px'}),
        #we include a title
        html.H1("IBD MAP FILTERS"),
        #we include a dropdown to filter the locality that we want to use as the origin
        html.Label('Choose a locality.',style={'margin-top': '40px', 'display': 'block','margin-bottom': '10px','font-size': '20px'}),
        dcc.Dropdown(
            id='dropdown-filter',
            options=[{'label': name, 'value': name} for name in localities[localities != '..']] ,
            value=None,
            placeholder="Select an option",
            style={'width': '600px','margin-left':'10px'}
        ),
        #we create a slider to decide the size of the hexagon that we want, the resolution
        html.Label('Choose the size of the hexagon',style={'margin-top': '40px', 'display': 'block','margin-bottom': '10px', 'font-size': '20px'}),
        dcc.Slider(
            id='Hexagon',
            min=2,
            max=4,
            step=0.25,
            value=3,
            included=False,
            marks={i: str(i) for i in [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4]}
        ),
        #we create a slider to define the length of the IBDs that we want to include in the map
        html.Label('Choose the length of the IBDs', style={'margin-top': '40px', 'display': 'block', 'margin-bottom': '10px','font-size': '20px'}),
        dcc.RangeSlider(
            id='range-slider-min-max',
            min=0,
            max=100000,
            step=100,
            value=[0, 100000],
            marks={i: str(i) for i in range(0, 100000, 5000)}
        ),
        #we include a submit button to move to the next step once they have finished selecting the filters
        html.Button('SUBMIT', id='submit-button', n_clicks=0, style={'float': 'right', 'margin-top': '25px',
                                                                    'font-size': '16px', 'width': '150px',
                                                                    'height': '50px', 'border-radius': '25px',
                                                                    'background-color': '#4CAF50', 'color': 'white', 'margin-bottom':'50px'}),
        
        html.Div(id='map-container'),
    ],
    style = {'margin-left': '90px','margin-right':'90px'})

    #this part of the code is to for a future modification, creating to separate windows, the first one with the filters, and the second one with the map
    # it also includes a return button
    '''
    layout2 = html.Div([
            html.Div([
            html.Img(src='https://www.dropbox.com/scl/fi/m9cmuqsgzxyjutdszbtzg/logoRojotop.png?rlkey=607jze6qiml76swqvhzt9j1nk&raw=1', style={'float': 'left','width': '370px', 'height': '100px', 'margin-top':'10px'}),
            html.Button('HOME', id='home-button', n_clicks=0, style={'float': 'right', 'margin-top': '40px', 'margin-right':'50px',
                                                                'font-size': '16px', 'width': '150px',
                                                                'height': '50px', 'border-radius': '25px',
                                                                'background-color': '#ABAAAA', 'color': 'white', 'margin-bottom':'30px'})],
            style={'width': '100%','height':'20%', 'display': 'inline-block'}),
            html.Div(style={'width': '100%', 'height':'85%', 'display': 'inline-block'}),
    html.Div(id='windowIn')])
    '''

    app.layout=layout1

    #we define the callback so we can continue to the next window with the map
    @app.callback(
        Output('map-container', 'children'),
        Input('submit-button', 'n_clicks'),
        Input('dropdown-filter', 'value'),
        Input('range-slider-min-max', 'value'),
        Input('Hexagon', 'value'))

    def map_window(n_clicks, dropdown_value, length, hexagon):
        print(n_clicks)
        if n_clicks:
            allhex,origin=filtering(nam,samples,dropdown_value,hexagon,length)
            allHex=coordinates(allhex, hexagon)
            map_layout=choropleth_map(allHex,origin, nam['Locality'], border_color = None, fill_opacity = 0.05, color_map_name = "Reds", initial_map = None)  
            return map_layout
    
    #this part of the code is also for the same double window modificiation
    '''
    @app.callback(
        Output('windowIn', 'children'),
        Input('home-button', 'n_clicks'))

    def home_window(n_clicks):
        if n_clicks:
            return layout1
    '''
    
    #we run the app 
    if __name__ == '__main__':
        app.run_server()


# Open the necessary files
with open("testingIBDData.tsv", "r") as DataBase:
    samples=pd.read_csv(DataBase, sep= '\t')

nam=pd.read_excel("AADRAnnotation.xlsx")
itself()

