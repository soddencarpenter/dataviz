/*
  This creates in the divvy database, the tables for the combined
   data that was given in the divvy_trip_history_201909-202108.csv
*/

CREATE DATABASE IF NOT EXISTS divvy
  CHARACTER SET UTF8MB4
  COLLATE utf8mb4_0900_ai_ci;

USE divvy;
DROP TABLE IF EXISTS divvy_trips;

CREATE TABLE divvy_trips (
  row_id LONG,
  id LONG,
  dot_1 LONG,
  ride_id VARCHAR(32) PRIMARY KEY,
  rideable_type VARCHAR(16),
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
  date DATE,
  month INT,
  day INT,
  year INT,
  day_of_week VARCHAR(12),
  INDEX usertype_idx(member_casual),
  INDEX start_time_idx(started_at),
  INDEX end_time_idx(ended_at),
  INDEX start_station_name_idx(start_station_name),
  INDEX end_station_name_idx(end_station_name)

);


