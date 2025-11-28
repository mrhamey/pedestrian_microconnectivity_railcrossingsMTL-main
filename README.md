# pedestrian_microconnectivity_railcrossingsMTL
This is the repository for my GEOG 464 project at Concordia University. The website displays pedestrian crossings of the CP rail right-of-way in Montréal QC and analyses the walksheds of various formal and informal crossings. 

File Structure
<pre>
.
├── site 
│   ├── styles.css
│   ├── compute_walksheds.py 
│   ├──graph_walksheds_ordered.html 
│   ├──walkshed_summaries.py
│   ├──mergingplaces_walkshed.py 
│   ├──resultsgraph.py 
│   ├──unique_walkshed_generator_test.py
│   ├── app.js
├── data
│   ├── places_with_walksheds.geojson
│   ├── places.geojson
│   ├── reachable_lines_400m.geojson
│   ├── reachable_lines_800m.geojson
│   ├── reachable_lines_400m_backup.geojson
│   ├── reachable_lines_800m_backup.geojson
│   ├── reseauvert.geojson
│   ├── roadnetwork_clipped_pedestrian_Cartiercrossing.geojson
│   ├── roadnetwork_clipped_pedestrian_default.geojson
│   ├── roadnetwork_clipped_pedestrian_Delepeecrossing.geojson
│   ├── roadnetwork_clipped_pedestrian_Gymcrossing.geojson
│   ├── roadnetwork_clipped_pedestrian_Skateparkcrossing.geojson
│   ├── roadnetwork_clipped_mtl_CLIPPED.geojson
│   ├── walkshed_network_lengths.csv
│
├── requirements.txt
├── bibliography.txt
├── index.html
├── LICENSE
└── README.md
</pre>



Acknowledgements: 

I would like to thank Professor Russell and Cameron Bruhbacker at Concordia University for teaching me everything I know about coding in Python. I would like to thank generative AI for assisting me with everything else that was needed for this project. 

Licence 
See the [licence](LICENSE) file


The project 
This project, designed to be viewed through the index.html file, contains a website exploring microconnectivity issues related to the CP Rail right-of-way in Montréal, QC. The project uses formal and informal crossings as a starting point to investigate the extent to which they allow for users to cross the rail right-of-way barrier. A walkshed is defined as the length of network that is accessible within a given distance from a crossing; 5 and 10 minute walksheds are used throughout this project to show how users might cross the rail in their local neighbourhood to access destinations on opposite sides. The walkshed can be expressed as either a sum of networks in meters (useful for comparing between crossings) or illustrated on the map to show areas that are better served by crossings. 

[Index.html:]( https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/index.html) 
This contains a Leaflet webmap (whose construction can be viewed in the app.js file) that displays the study area and its formal, informal, and under-construction crossings. Clicking on a crossing displays its 400m (5-minute) and 800m(walkshed) to show what area of the road network is within that distance from the crossing. The webmap is complemented by a legend, as well as information tabs explaining the project, the history of the area, the results of my research, as well as a discussion of methods and limitations. Regarding the results, a plotly graph is included to visually illustrate the total sums of the network within the walksheds of the crossings. 

[requirements.txt:](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/requirements.txt)  standard required package file to ensure that users have all required packages to copy and use my algorithms.

[/Site:](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/tree/main/site)
The site folder contains the app.js file that builds the Leaflet webmap. It also contains various python files used to create the walksheds. 
- [styles.css](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/site/styles.css ) is the css file that structures my index.html and styles its elements. Also contains the style classes for the webmap and its legend. 
- [Compute_walksheds.py](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/site/compute_walksheds.py) contains the algorithm used to associate crossings to the relevant network file, construct a network graph using the networkx package, calculate the road segments that are within 400m and 800m of the origin point, and then generate a new reachable_lines_XXXm.geojson file containing these features (and a backup). 
- [Walkshed_summaries.py](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/site/walkshed_summaries.py) reads the reachable_lines_XXXm.geojson file and sums together the lengths of the walkshed segments to generate the total length of network in the walkshed, which is then exported into walkshed_network_lengths.csv (see /data file explanations)
    - [mergingplaces_walksheds.py](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/site/mergingplaces_walkshed.py) then attributes these sums to the crossings (places.geojson) in order to be able to display these attributes on the webmap. 
- [resultsgraph.py](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/site/resultsgraph.py) builds the plotly graph to show the two walksheds overlapped on one bar, with crossings arranged and named west-east. 
    - This is then exported to [graph_walksheds_ordered.html](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/site/graph_walksheds_ordered.html) in order to be referenced within index.html to display in the results infotab; preserving and exporting it as HTML maintains its interactivity, allowing users to zoom and hover for specific walkshed information. 
- [unique_walkshed_generator_test.py](https://github.com/mrhamey/pedestrian_microconnectivity_railcrossingsMTL-main/blob/main/site/unique_walkshed_generator_test.py) is an unfinished algorithm that was intended to generate a new layer that would show the network segments that are included only in the informal crossings, to show viewers on the map the area of the network that are within these informal crossings’ walksheds, and thus could be used to show which informal crossings would lead to the greatest increase in connectivity. 
    - However, the algorithm does not function as intended and includes many segments that are clearly within the walkshed of other crossings. Due to a lack of resources, I was unable to refine this further and try to come up with a solution.

/Data: 
The [/data](/data) folder contains all data files used for the construction of my web map

- [places.geojson](/data/places.geojson) is a collection of all informal, formal, and under-construction crossings of the CP rail right-of-way in the study area.
- [places_with_walksheds.geojson](/data/places_with_waksheds.geojson) contains the same information as places.geojson, just with the walkshed summary info added to it (see /site file explanations)

- The [reseauvert.geojson](/data/reseauvert.geojson) contains a line corresponding to the mixed-use Reseau Vert trail, the length of the corridor, to better illustrate the study area
- [reachable_lines_400m.geojson](/data/reachable_lines_400m.geojson)  + backups contain the walksheds of each crossing, composed of line segments, calculated in compute_walksheds.py (see /site file explanations)
          - see [reachable_lines_800m.geojson](/data/reachable_lines_800m.geojson) for the equivalent but at the larger, 10 minute walkshed. 

[roadnetwork_clipped_pedestrian_default.geojson](/data/roadnetwork_clipped_pedestrian_default.geojson) is the road network file provided by the City of Montréal with some additional geometries added by me in order to integrate the various pedestrian paths (ex. Réseau vert) in the area. This file notably lacks all networks associated with the informal or under-construction crossings, such that the walkshed for formal crossings does not integrate any additional connectivity provided by the informal or under-construction crossings. 

The other roadnetwork_clipped_pedestrian_XXX.geojson files (ex. [roadnetwork_clipped_pedestrian_Cartiercrossing.geojson](/data/roadnetwork_clipped_pedestrian_Cartiercrossing.geojson)are copies of this file but with changes for the informal and underconstruction crossings, such that the road network actually reflects access through these unofficial crossings. 
- [Outdoor_Gym_Crossing_uniquewalkshed.geojson](/data/Outdoor_Gym_Crossing_uniquewalkshed.geojson) is a test unique walkshed file that shows the additional network added to the walksheds around the CP Rail right-of-way. It shows the issues in the algorithm (areas clearly within the walkshed of other crossings) and should not be considered for analysis. Again, for illustrative purposes only. 


FAQ 
Why does there appear to be floating network segments? 
This is due to the configuration and properties of my source road network file. Some road segments were still considered part of another segment despite being unconnected; therefore, they were considered to be part of the walkshed if the ‘parent’ segment was still within the area. 

Why do all walksheds appear to end at segment ends rather than at a true 400m walkshed?  - This is because I was unable to troubleshoot why my algorithm which purported to cut the segments at the 400m-along-network-from-node, evidently did not do the cutting 

Why were you unable to calculate the informal crossings that led to the greatest increase in network connectivity? 
Again, similar to the question above about floating network segments, the configuration of my base road network was unable to properly compute network segments belonging to only one crossing’s walkshed. When trying to filter my walkshed data for the road segments that appear only in one crossing, there were many road segments included that were visibly within the walkshed of other crossings. I ran out of time to troubleshoot this further. 

Do you have further plans for this project?  - I think it would be interesting to spend the time required to fix the algorithms and see if proper computation is possible. I think the solution lies somewhere in finding and configuring a better road network file. A larger project to undertake would be to create a website capable of computing walksheds based on user-submitted road, rail, and crossing network data, such that other cities’ connectivity issues could be properly analyzed. 
