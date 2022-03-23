CREATE DATABASE IF NOT EXISTS divvy
  CHARACTER SET UTF8MB4
  COLLATE utf8mb4_0900_ai_ci;

USE divvy;
DROP TABLE IF EXISTS divvy_2019;
CREATE TABLE divvy_2019 (
  trip_id VARCHAR(32) PRIMARY KEY,
  start_time DATETIME,
  end_time DATETIME,
  bikeid VARCHAR(32),
  tripduration_raw VARCHAR(16),
  from_station_id LONG,
  from_station_name VARCHAR(255),
  to_station_id LONG,
  to_station_name VARCHAR(255),
  usertype VARCHAR(32),
  INDEX usertype_idx(usertype)
);
