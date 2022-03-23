#!/bin/bash

script=$HOME/dataviz/proc.py

if [[ -n $1 ]]; then
    f=$1
    of=${f%.csv}-conv.csv
    echo "Single Processing $f to $of"   
    python $script --file $f > $of
else
  for f in Divvy_Trips_*.csv 202*.csv; do
    of=${f%.csv}-conv.csv
    echo "Processing $f to $of"   
    python $script --file $f > $of
  done
fi