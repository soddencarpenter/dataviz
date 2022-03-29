# This is a quick exploration of some divvy bike data

# dataset is at d:/DivvyDatasets
# divvy_tip_history_201909-202108.csv

install.packages("ggplot2")
install.packages("tidyverse")
install.packages("readxl")
install.packages("here")
install.packages("skimr")
install.packages("kableExtra")
install.packages("zoo")

install.packages("data.table")
install.packages('dplyr')

install.packages('googleway')
install.packages('ggmap')
install.packages('maps')


library(ggplot2)
library(tidyverse)
library(readxl)
library(here)
library(skimr)
library(kableExtra)
library(zoo)

# helps with data import

library(data.table)

# allows for select like approach

library(dplyr)

# default way to load
# divvy <- read.csv('~/Downloads/divvy_trip_history_201909-202108.csv', sep=",")

# a faster way to load using data.table
remove(divvy)
gc()
divvy <- data.table::fread('d:/DivvyDatasets/divvy_trip_history_201909-202108.csv')

# just gives some quick data on what has been loaded
head(divvy)  # first few rows
str(divvy)   # STRucture of the dataset

# load temperature data
chitemp <- data.table::fread('d:/DivvyDatasets/ChicagoTemperature.csv')
head(chitemp)


#
#
# we want to have the temperature added to the divvy dataset
#
#
divvy = merge(divvy,chitemp)


head(divvy)
str(divvy)

# get by col numbers
divvy[, c(1,7,8)]

divvy[, c('date','started_at','ended_at','avg_temperature_fahrenheit')]


#
# add a year-month display
#
divvy$yrmo <- as.yearmon(paste(divvy$year, divvy$month), "%Y %m")

#
#
# add a calculated duration; minutes makes more sense
#
#
divvy$duration = as.numeric(difftime(divvy$ended_at, divvy$started_at, units='min'))


divvy[, c('start_station_name', 'end_station_name', 'duration')]

# show the maximum and minimum rows
divvy[which.max(divvy$duration)]
divvy[which.min(divvy$duration)]


#
# clean the dataset
#
remove(divvy_too_short)
remove(divvy_too_long)

# there are several instances where the ride is too short
divvy_too_short = subset(divvy, divvy$duration < 1.2)
divvy_too_short[, c('date','rideable_type','started_at','ended_at','duration','start_station_name', 'end_station_name')]

nrow(divvy_too_short)
nrow(divvy)
divvy = anti_join(divvy, divvy_too_short)
nrow(divvy)

# and some instances of the ride too long; it may be chargeable, but it
#  isn't great data
divvy_too_long = subset(divvy, divvy$duration > 60 * 12)
nrow(divvy_too_long)
divvy_too_long[, c('date','member_casual','rideable_type','started_at','ended_at','duration','start_station_name', 'end_station_name')]
nrow(divvy_too_long)
nrow(divvy)
divvy = anti_join(divvy, divvy_too_long)
nrow(divvy)

remove(divvy_members)
remove(divvy_casual)
divvy_members = subset(divvy, divvy$member_casual =='member')
nrow(divvy_members)
divvy_casual = subset(divvy, divvy$member_casual == 'casual')
nrow(divvy_casual)
mean(divvy$duration)
mean(divvy_members$duration)
mean(divvy_casual$duration)


#
# find top stations for members by month
#
remove(members_start)

members_start <- divvy_members %>%
  group_by(yrmo, start_station_name) %>%
  summarize(rides_by_monthyear =  n())  %>%
  spread(yrmo, rides_by_monthyear)
str(members_start)
members_start$total <- rowSums(members_start[, c(2:25)], na.rm=TRUE)
members_start <- members_start[order(-members_start$total),]
head(members_start)
members_start <- members_start[2:21,] #drop 1st row; exclude NA @ start, top 20
# set stations as row names
members_start <- as.data.frame(members_start)
row.names(members_start) <- members_start$start_station_name
members_start <- members_start[,2:25] # drop col w/station name, total
members_start <- members_start[order(row.names(members_start)),]
members_start

nrow(members_start)
members_start <- rbind(members_start,c(colSums(members_start)));
members_start
#fwrite(members_start, 'd:/DivvyDatasets/top_member_stations.csv', row.names = TRUE)


#
# find top stations for casual by month
#
remove(casual_start)
casual_start <- divvy_casual %>%
  group_by(yrmo, start_station_name) %>%
  summarize(rides_by_monthyear =  n())  %>%
  spread(yrmo, rides_by_monthyear)
str(casual_start)
casual_start$total <- rowSums(casual_start[, c(2:25)], na.rm=TRUE)
casual_start <- casual_start[order(-casual_start$total),]
head(casual_start)
casual_start <- casual_start[2:21,] #exclude NA @ start, top 20
# set stations as row names
casual_start <- as.data.frame(casual_start)
row.names(casual_start) <- casual_start$start_station_name
casual_start <- casual_start[,2:25] # drop col w/station name, total
casual_start <- casual_start[order(row.names(casual_start)),]
casual_start <- rbind(casual_start,c(colSums(casual_start)));
casual_start

#fwrite(casual_start, 'd:/DivvyDatasets/top_casual_stations.csv', row.names = TRUE)



