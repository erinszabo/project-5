# UOCIS322 - Project 5 #

## Erin Szabo
#### Fall 2023
### eszabo@uoregon.edu

Brevet time calculator with MongoDB!

## Overview

In this project, we take the brevet calculator created in project 4 and introduce database functionality using MongoDB.


## Getting started

With Docker running, use the following command:

```
docker compose up
```

Then navigate to your local host (port 5001). The calculator page should be up and running, this time with a `Submit` and `Display` button.

After selecting a brevet distance and entering some control times, click `Submit` to send this data to the brevet database using MongoDB. When the page is refreshed, the data is cleared. Click `Display` to display the most recent brevet information stored in the database.

## Rules
 - select a brevet distance: 200km, 300km, 400km, 600km, 1000km

 - enter the distance from the starting point to the control location

  	- optionally enter the name of the control location
		
   - once a control distance is entered, the opening and closing times for this control location will be calculated and displayed		
 
 - the final control location must be no further than 20% of the total selected brevet distance

- the first control location may be "relaxed" if it is close enough to the starting point, meaning there will always be at least an hour before the first control location is closed

## Original Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.
