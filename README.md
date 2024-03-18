
<h3>PROJECT BINP29 - MSc IN BIOINFORMATICS - LUNDS UNIVERSITY</h3>
BORJA MEDINA DE LAS HERAS

<h1> VISUALIZE ANCIENT IBD CONNECTIONS ON A MAP </h1>

<h4> FINAL IDEA - CREATING POPUALTIONS USING HEXAGONS (h3 software)</h4>
I'm going to use hexagons to divide the locations into different populations.

More darker the populations with more counts.  
I'm going to stick with counts.  

Here I have two posibilities:  
>1. Counting the number of times an hexagon appears and drawing just one hexagon with an specific colour. This way would be faster, but porbably we won't be able to see to much, because the closest popualtions usually have a really really high number of counts, so you would only see those in the map.
> 
>2. Instead of counting, drawing all hexagons but with a really low alpha, so we would see darker the places in which we have more number of hexagons. Instead of having a maximum, we have a minimum, so if you are somehow related we would see it in the map, if you are higly related we would see it too, but if you are really really high related, we will just see it as high related.

I have decided to start with this last option, I might change in the future.  

<h5> Functions </h5>

>1. Import some libraries.  
>2. hexagons_dataframe_to_geojson() transforma pandas datafram with hexagons to a geojson format.  
>3. Filtering(): filtering the samples database.  
>4. coordinates(): cacualte the hexagon using the coordinates.  
>5. cloropleth_map(): draqing the hexagons and creating the layout.

After the fucntions, we just open the files and run the functions in order to get the app and run it on the server as an interactive map.

<h5>Modifications needed</h5>
It's a really slow code even thought we are using a smaller verison of the data, with just one popualtion, and therefore the filtering we have to do is much lower.  
I have to find a way to make it faster. Using dictionaries are an option to make faster some of the loops.  
Also I want to make it more interactive, create a first window, and filtering in that specific window.  
I have to code it to filter through the whole databases.


<h4>DISCARDED IDEA - BOUNDARIES USING POLITICAL MAP</h4>
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

Also a problem are the populations, that doesn't represent real popualtions.  
Also I have to add the filtering of the data for a apsecific population.  
I have to make it interactive (Dash).
