PROJECT BINP29 - MSc IN BIOINFORMATICS - LUNDS UNIVERSITY
BORJA MEDINA DE LAS HERAS

VISUALIZE ANCIENT IBD CONNECTIONS ON A MAP

I'm going to get a subset the IBD file to start working with.
The more IBDs a population share the more closely they are genealogically.
Count the number of IBDs and paint a heatmap.
To paint the map I'm using a political map with the actual boundaries.



HeatMap: it was created using a smaller dataset that contained info of only one population.
It creates a heatmap with the actual political boundaries.
	Import some libraries
	Get the ids and the coordinates
	Get the countries using the coordinates(the decision of doing this instead of using the countrie names present in the ADDR table was that it contains a lot of misspellings)
	Get the counts and the sum of the lengths (I wasn't sure if I wanted to use the counts or the lengths when drawing the heatmap).
	Draw the map
	Save the map
This code is really slow and I have to create functions so I can call them back.
Also a problem are the populations, that doesn't represent real popualtions. 
Also I have to add the filtering of the data for a apsecific population.
I have to make it interactive (Dash).