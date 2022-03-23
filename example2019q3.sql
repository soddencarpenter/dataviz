create database divvy;

use divvy;

create table 2019q3 (
  trip_id VARCHAR(32),
  start_time DATETIME,
  end_time DATETIME,
  bikeid VARCHAR(16),
  tripduration VARCHAR(12),
  from_station_id VARCHAR(12),
  from_station_name VARCHAR(48),
  to_station_id VARCHAR(12),
  to_station_name VARCHAR(48),
  usertype VARCHAR(16),
  gender VARCHAR(12),
  birthyear int default 0

  );



  
  drop table 2019q3;
  
/*  
load data infile 'c:/Users/khols/OneDrive/Documents/Training & Learning/DataVisualization - 2022-03-15/Datasets/divvy/Divvy_Trips_2019_Q3.csv'
*/
/*
 load data infile 'c:/Users/khols/OneDrive/Documents/Training & Learning/DataVisualization - 2022-03-15/Datasets/divvy/a'
 */
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