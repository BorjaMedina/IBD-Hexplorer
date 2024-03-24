
<h1>IBD Hexplorer</h1>

![Image](https://www.dropbox.com/scl/fi/m9cmuqsgzxyjutdszbtzg/logoRojotop.png?rlkey=607jze6qiml76swqvhzt9j1nk&raw=1)

<h3>PROJECT BINP29 - MSc IN BIOINFORMATICS - LUNDS UNIVERSITY</h3>
BORJA MEDINA DE LAS HERAS

<h2> VISUALIZE ANCIENT IBD CONNECTIONS ON A MAP </h2>

IBD Hexplorer represents the genealogical relatedness between a selecetd ancient location and the worlds ancient popualtions. All the representations are based in the analysis of shared IBD segments information.

Through this README file we are going to go through the IBD Hexplorer app.
We are going to introduce all the versions and modificatiosn made throught the file history.  
Starting with the newest (actual v0.1) versions. At the end of the README the initial idea (oldest version of the app).

<h4> IBD HEXPLORER - FINAL APP - v0.1 </h4>

Command to run the app:

	python IBDHexplorer.py

It will open an interactive window with the possible filters.  
After selecting the filters wanted press submit.

IMPORTANT: the app uses the IBD dataset and the ADDR dataset. Both datasets are neede for the app to run.  
In case you want to try the app with a smaller dataset there is a testing dataset in the repository (IBD_testDataset). If you want to run the app with this dataset you have to modify the last lines of the script in which we open the files needed (line 250, change "ibd220.ibd.v54.1.pub" for the anme of your IBD file).  
It's important to be aware that this testing dataset includes only IBD segments related with Bohemia population, and therefore it doesn't make sense to run the app choosing other population than Bohemia because the result will always be a genealogical relationship with Bohemia population.  
With the whole IBD dataset ("ibd220.ibd.v54.1.pub", not presesent in the repository) you can choose whatever population is available.

<h5> Functions </h5>

>1. Import some libraries.  
>2. Filtering(): filtering the samples database. A better filtering fucntion for the whole database.  
>3. coordinates(): cacualte the hexagon using the coordinates.  
>4. cloropleth_map(): drawing the hexagons and creating the layout. Including a better layout.
>5. itself(): contains the main code (first layout and callbacks).

Be aware of some errors and some future modfications:

>1. If the user modifies a filter (after running the first time) it updates before pressing submit again, because the variable “n_clicks” of the callback is not reset to 0. The app still works but it can cause troubles if the user wants to modify more than one filter at a time.
>2. We have created the script so we can add another filter to differentiate the initial population size and the drawing population size.
>3. We want to add some other filtering options, including antiquity of the samples.
>4. We want to create some error messages when there is no IBD segments found for the filters selected. Right now we don’t have error handling for the filters and therefore the app crashes.
>5. Create a two independant window app.

-------------------------------------------------------------------------
OLDER VERSIONS OF THE APP.
This is not anymore part of the final IBD HExplorer app, but it contains the evolution of the script until the creation of the final app.

This part of the README is merely academic. It doesn't include information about how to use the real application.  

-----
<h4> MODFICATION OF SECOND IDEA - CREATING POPUALTIONS USING HEXAGONS (h3 software)</h4>
Running scrip in the terminal:

	 python IBDHExplore.py < population >

If you dont specify any population it will run with the default one ('Madrid, Humanejos').

I'm going to use hexagons to divide the locations into different populations.  
More darker the populations with more IBD counts.

Changes respect the previous script: includes a full filtering function and a more interactive layout.
Also it can be run from terminal using the running command above.

<h5> Functions </h5>

>1. Import some libraries.  
>2. Filtering(): filtering the samples database. A better filtering function for the whole database.  
>3. coordinates(): calculate the hexagon using the coordinates.  
>4. cloropleth_map(): drawing the hexagons and creating the layout. Including a better layout.

After the functions, we just open the files and run the functions in order to get the app and run it on the server as an interactive map.

<h5>Modifications needed</h5>
It's still really slow, specially the filtering.
The interactive part is not working, I have to make the callback so it works.
I have to add a way of filtering by length and also a way to select the size of the hexagons interactively.

-----
<h4> SECOND IDEA - CREATING POPULATIONS USING HEXAGONS (h3 software)</h4>
I'm going to use hexagons to divide the locations into different populations.

More darker the populations with more counts.  
I'm going to stick with counts.  

Here I have two posibilities:

>1. Counting the number of times an hexagon appears and drawing just one hexagon with an specific colour. This way would be faster, but probably we won't be able to see to much in the map, because the closest populations usually have a really really high number of counts, so you would only see those in the map (the rest would be all of them really low).
>2. Instead of counting, drawing all hexagons but with a low alpha, so we would see darker the places in which we have more number of hexagons. Instead of having a maximum, we have a minimum, so if you are somehow related we would see it in the map, if you are higly related we would see it too, but if you are really really high related, we will just see it as high related.

I have decided to start with this last option, I might change in the future.  

<h5> Functions </h5>

>1. Import some libraries.  
>2. hexagons_dataframe_to_geojson() transform a pandas dataframe with hexagons to a geojson format.  
>3. Filtering(): filtering the samples database.  
>4. coordinates(): caculate the hexagon using the coordinates.  
>5. cloropleth_map(): drawing the hexagons and creating the layout.

After the functions, we just open the files and run the functions in order to get the app and run it on the server as an interactive map.

<h5>Modifications needed</h5>
It's a really slow code even thought we are using a smaller subset of the data, with just one population, and therefore the filtering we have to do is much lower.  
I have to find a way to make it faster. Using dictionaries is an option to make faster some of the loops.  
Also I want to make it more interactive, create a first window, and filtering in that specific window.  
I have to code it to filter through the whole databases.

-----
<h4>DISCARDED IDEA - BOUNDARIES USING POLITICAL MAP - IBDheatMap.py</h4>
I'm going to get a subset the IBD file to start working with.  
The more IBDs a population share the more closely they are genealogically.

Count the number of IBDs and paint a heatmap.  
To paint the map I'm using a political map with the actual boundaries.  

HeatMap: it was created using a smaller dataset that contained info of only one population. It creates a heatmap with the actual political boundaries.  
>1. Import some libraries  
>2. Get the ids and the coordinates  
>3. Get the countries using the coordinates(the decision of doing this instead of using the countrie names present in >the ADDR table was that it contains a lot of >misspellings)  
>4. Get the counts and the sum of the lengths (I wasn't sure if I wanted to use the counts or the lengths when drawing the heatmap).  
>5. Draw the map  
>6. Save the map

<h5>Modifications needed</h5>
This code is really slow and I have to create functions so I can call them back.

Also a problem are the populations, that doesn't represent real populations.  
Also I have to add the filtering of the data for a specific population.  
I have to make it interactive (Dash).
