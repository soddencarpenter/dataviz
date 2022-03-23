#!/bin/bash

base=https://divvy-tripdata.s3.amazonaws.com

for f in $(seq 1 4); do
	wget $base/Divvy_Trips_2019_Q${f}.zip
done


wget $base/Divvy_Trips_2020_Q1.zip

for f in $(seq -f "%02g" 4 12); do
	wget $base/2020${f}-divvy-tripdata.zip
done

for f in $(seq -f "%02g" 1 12); do
	wget $base/2021${f}-divvy-tripdata.zip
done
