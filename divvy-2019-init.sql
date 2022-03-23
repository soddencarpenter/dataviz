/*
  This creates in the divvy database, the table for the 2019 dataset
    for importing the data directly from the .csv files.

  It is designed to allow each year to be in a separate table.
  
  With the schema differences between 2019 and 2020, the datasets cannot
    be directly combined in a raw import.

  In cotrast to the 2020, and the 2021 datasets, this dataset has:
    + bikeid
    + tripduration
    + gender, birthyear
    + usertype instead of member_casual
    - no latitude and longitude
    * different station ids
*/


CREATE DATABASE IF NOT EXISTS divvy
  CHARACTER SET UTF8MB4
  COLLATE utf8mb4_0900_ai_ci;

USE divvy;
DROP TABLE IF EXISTS divvy_2019;
CREATE TABLE divvy_2019 (
  trip_id VARCHAR(32) PRIMARY KEY,
  start_time DATETIME,
  end_time DATETIME,
  bikeid VARCHAR(16),
  tripduration VARCHAR(16),
  from_station_id LONG,
  from_station_name VARCHAR(48),
  to_station_id LONG,
  to_station_name VARCHAR(48),
  usertype VARCHAR(32),
  gender VARCHAR(12),
  birthyear int default 0,
  INDEX usertype_idx(usertype),
  INDEX start_time_idx(start_time),
  INDEX end_time_idx(end_time),
  INDEX start_station_name_idx(from_station_name),
  INDEX end_station_name_idx(to_station_name)

);
