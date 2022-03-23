use divvy;
desc divvy_2019;

/*
load data infile 'c:/Users/khols/OneDrive/Documents/Training & Learning/DataVisualization - 2022-03-15/Datasets/divvy/Divvy_Trips_2019_Q3.csv'
  into table 2019q3
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 rows
  (trip_id,start_time,end_time,bikeid,tripduration,from_station_id,from_station_name,
   to_station_id,to_station_name,usertype,@vgender,@vbirthyear)
   SET birthyear = NULLIF(@vbirthyear,'')
  ;
  */

load data infile 'c:/Users/khols/OneDrive/Documents/Training & Learning/DataVisualization - 2022-03-15/Datasets/divvy/Divvy_Trips_2019_Q1-trunc.csv'
  into table divvy_2019
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 rows;
  
  load data infile 'c:/Users/khols/OneDrive/Documents/Training & Learning/DataVisualization - 2022-03-15/Datasets/divvy/Divvy_Trips_2019_Q2-trunc.csv'
  into table divvy_2019
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 rows;
  
  load data infile 'c:/Users/khols/OneDrive/Documents/Training & Learning/DataVisualization - 2022-03-15/Datasets/divvy/Divvy_Trips_2019_Q3-trunc.csv'
  into table divvy_2019
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 rows;
  
  load data infile 'c:/Users/khols/OneDrive/Documents/Training & Learning/DataVisualization - 2022-03-15/Datasets/divvy/Divvy_Trips_2019_Q4-trunc.csv'
  into table divvy_2019
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 rows;