/*
  This creates in the divvy database, the tables for 2020 and 2021
   for allowing importing of the data directly from the .csv files.

   It is designed to allow each year to be in a separate table

   In contrast to the 2019 dataset, these data have:
      + latitude and longitude
      + member_casual instead of usertype
      - no tripduration
      - no bikeid
      - no gender, birthyear
*/

CREATE DATABASE IF NOT EXISTS divvy
  CHARACTER SET UTF8MB4
  COLLATE utf8mb4_0900_ai_ci;

USE divvy;
DROP TABLE IF EXISTS divvy_2020;
DROP TABLE IF EXISTS divvy_2021;

CREATE TABLE divvy_2020 (
  ride_id VARCHAR(32) PRIMARY KEY,
  rideable_type VARCHAR(16)
  started_at DATETIME,
  ended_at DATETIME,
  start_station_name VARCHAR(48),
  start_station_id LONG,
  end_station_name VARCHAR(48),
  end_station_id LONG,
  start_lat DOUBLE,
  start_lng DOUBLE,
  end_lat DOUBLE,
  end_lng DOUBLE,
  member_casual VARCHAR(32),
  INDEX usertype_idx(member_casual),
  INDEX start_time_idx(started_at),
  INDEX end_time_idx(ended_at),
  INDEX start_station_name_idx(start_station_name),
  INDEX end_station_name_idx(end_station_name)

);


CREATE TABLE divvy_2021 (
  ride_id VARCHAR(32) PRIMARY KEY,
  rideable_type VARCHAR(16)
  started_at DATETIME,
  ended_at DATETIME,
  start_station_name VARCHAR(48),
  start_station_id LONG,
  end_station_name VARCHAR(48),
  end_station_id LONG,
  start_lat DOUBLE,
  start_lng DOUBLE,
  end_lat DOUBLE,
  end_lng DOUBLE,
  usertype VARCHAR(32),
  INDEX usertype_idx(usertype),
  INDEX start_time_idx(started_at),
  INDEX end_time_idx(ended_at),
  INDEX start_station_name_idx(start_station_name),
  INDEX end_station_name_idx(end_station_name)

);

