import pandas as pd
import numpy as np
import datetime as datetime
import pandas.api.types as pt

from pathlib import Path


rev = "3"

input_dir = '/mnt/d/DivvyDatasets'
input_divvy_basename = "divvy_trip_history_201909-202108"
input_divvy_base = input_dir + "/" + input_divvy_basename
input_divvy_raw = input_divvy_base + ".csv"
input_divvy_rev = input_dir + "/rev" + rev + "-" + input_divvy_basename + ".csv"
input_chitemp = input_dir + "/" + "ChicagoTemperature.csv"


#
#  returns true if the rev file is already present
#
def rev_file_exists():
  path = Path(input_divvy_rev)
  return path.is_file()




def update_dow_to_category(df):
  #
  # we need to get the dow properly set
  #
  cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

  cats_type = pt.CategoricalDtype(categories=cats, ordered=True)
  df['day_of_week'] = df['day_of_week'].astype(cats_type)

  return df



#
# loads and returns the rev file as a data frame. It handles
#   the need to specify some column types
#
#  filename : the filename to load
#
def load_divvy_dataframe(filename):
  print("Loading " + filename)
  # so need to set the type on a couple of columns
  col_names = pd.read_csv(filename, nrows=0).columns
  types_dict = { 'ride_id': str, 
    'start_station_id': str,
    'end_station_id': str,
    'avg_temperature_celsius': float,
    'avg_temperature_fahrenheit': float,
    'duration': float,
    'start_lat': float,
    'start_lng': float,
    'end_lat': float,
    'end_lng': float,
    'avg_rain_intensity_mm/hour': float,
    'avg_wind_speed': float,
    'max_wind_speed': float,
    'total_solar_radiation': int
    }
  types_dict.update({col: str for col in col_names if col not in types_dict})

  return pd.read_csv(filename, dtype=types_dict)



def yrmo(year, month):
    return "{}-{}".format(year, month)




def calc_duration_in_minutes(started_at, ended_at):
    st = datetime.datetime.strptime(started_at, '%Y-%m-%d %H:%M:%S')
    en = datetime.datetime.strptime(ended_at, '%Y-%m-%d %H:%M:%S')
    diff = en - st
    return diff.total_seconds() / 60




#
# load the chicago temperature into a data frame
#
def load_temperature_dataframe():
  print("Loading " + input_chitemp)
  return pd.read_csv(input_chitemp)




#
# handles loading and processing the divvy raw data by
#   adding columns, removing bad data, etc.
#
def process_raw_divvy(filename):
  df_divvy = load_divvy_dataframe(filename)

  df_chitemp = load_temperature_dataframe()

  #
  # add a year-month column to the divvy dataframe
  #  this uses a function with the row; it is not
  #  the absolute fastest way
  #
  print("Adding year-month as yrmo")
  df_divvy['yrmo'] = df_divvy.apply(lambda row: yrmo(row['year'], row['month']),
                                      axis = 1)

  #
  # we also want a duration to be calculated
  #
  print("Adding duration")
  df_divvy['duration'] = df_divvy.apply(lambda row: calc_duration_in_minutes(row['started_at'],
                                                      row['ended_at']),
                                      axis = 1)

  #
  # add the temperature
  #
  print("Merging in temperature")
  df_divvy = pd.merge(df_divvy, df_chitemp,
    on="date")
  print(df_divvy.shape)
  print(df_divvy.head())
  # print(df_divvy.loc[df_divvy['date'] == '2020-02-21']) # 2020-02-21 was missing in org. temp

  print(df_divvy.info())  # shows mem usage, other info
  print(df_divvy[['ride_id','member_casual','date','duration','yrmo','avg_temperature_fahrenheit']])

  #
  # clean the dataframe to remove invalid durations
  #   which are really only (about) < 1 minute, or > 12 hours
  #
  print("Removing invalid durations")
  df_divvy = df_divvy[(df_divvy.duration >= 1.2) & (df_divvy.duration < 60 * 12)]
  print(df_divvy.shape)

  df_divvy = update_dow_to_category(df_divvy)

  #
  # drop some bogus columns
  #
  df_divvy.drop(df_divvy.columns[[0,30]], axis=1, inplace=True)

  return df_divvy




#
# writes the dataframe to the specified filename
#
def save_dataframe(df, filename):
  print("Saving dataframe to " + filename)
  df.to_csv(filename, index=False)


#
# load the divvy csv into a data frame
#
if rev_file_exists():
  df_divvy = load_divvy_dataframe(input_divvy_rev)
  df_divvy = update_dow_to_category(df_divvy)
else:
  df_divvy = process_raw_divvy(input_divvy_raw)
  save_dataframe(df_divvy, input_divvy_rev)

print(df_divvy)
df_divvy.info()






#
# btw, can just pass the row and let the function figure it out
#
#def procone(row):
#    print(row['date'])
#    return 0
#df_divvy.apply(lambda row: procone(row), axis = 1)





