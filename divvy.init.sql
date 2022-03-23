/*
 creates a table for the fully divvy converted import
 */

use divvy; 

CREATE DATABASE IF NOT EXISTS divvy
  CHARACTER SET UTF8MB4
  COLLATE utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS divvy;

 CREATE TABLE divvy (
  trip_id VARCHAR(32) PRIMARY KEY,
  rideable_type VARCHAR(32),
  usertype VARCHAR(32),
  start_time DATETIME,
  end_time DATETIME,
  tripduration DOUBLE,
  start_station_name VARCHAR(48),
  start_station_id LONG,
  org_start_station_id LONG,
  end_station_name VARCHAR(48),
  end_station_id LONG,
  org_end_station_id LONG,
  start_lat DOUBLE,
  start_lng DOUBLE,
  end_lat DOUBLE,
  end_lng DOUBLE,
  quarter INT,
  month INT,
  year INT,
  day_of_week INT,
  INDEX usertype_idx(usertype),
  INDEX start_time_idx(start_time),
  INDEX end_time_idx(end_time),
  INDEX start_station_name_idx(start_station_name),
  INDEX end_station_name_idx(end_station_name),
  INDEX year_idx(year),
  INDEX month_idx(month)
 );
 
   
