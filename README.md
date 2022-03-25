# dataviz
Some scripts for the Data Visualization class


## Divvy 2019 Data
The Divvy 2019 data from the files Divvy_Trips_2019_Q?.csv
may be imported in the following manner.

1. Create a divvy database and a table divvy_2019
    (see divvy-2019-init.sql)

1. Generate the import sql
   $ gen-2019-import-sql.sh > divvy2019imp.sql

1. Import the data
   (mysql in the appropriate directory; logged in)
   mysql> use divvy;
   mysql> source divvy2019imp.sql;

Note there are several differences in the 2019 data from later datasets
1. The gender and birthyear are not present in later datasets
1. The tripduration is not present in later datasets
1. The usertype is Customer/Subscriber; in later datasets it is 
   casual/member
1. The 2019 datasets do not have the rideable type, nor do they have
   the lat and lng for the starting and ending points

## Converting all datasets
1. To normalize all of the datasets, it is possible to use the
    proc.py script. This script will take a divvy .csv file, and
    convert it to a common format. It will calculate trip duration,
    add lat and lng, update station ids, update Customer/Subscriber.
1. See the process.sh script for invocation

### Schema and Importing
1. Create the divvy database and a table divvy
   (see divvy.init.sql)

1. Generate the import sql
   $ gen-import-sql.sh > divvyimp.sql

1. Import the data
   (mysql in the appropriate directory; logged in)
   mysql> use divvy;
   mysql> source divvyimp.sql;


## divvy_trip_history_201909-202108.csv set
This is the dataset for class 4 "Divvy heatmap data". 

1. Create the divvy database
1. divvy-triphistory-init.sql will create a table divvy_trips
1. The gen-triphistory-import-sql.sh will generate an import statement


