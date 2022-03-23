#!/bin/bash

table=divvy_2019

curdir=$(wslpath -m .)

function appendTo() {
    local f=$1

cat << EOF
load data infile "${curdir}/$f"
  into table $table
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 rows
  (trip_id,start_time,end_time,bikeid,tripduration,from_station_id,from_station_name,
    to_station_id,to_station_name,usertype,@vgender,@vbirthyear)
  SET birthyear = NULLIF(@vbirthyear,'')
;

EOF
}


if [[ $# -eq 0 ]]; then
    for f in Divvy_Trips_2019_Q?.csv; do
      appendTo $f
    done
else
    for f in $*; do
        appendTo $f
    done
fi