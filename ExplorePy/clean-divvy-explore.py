import pandas as pd
import numpy as np
import datetime as dt
import pandas.api.types as pt
import pytz as pytz

from astral import LocationInfo
from astral.sun import sun
from astral.geocoder import add_locations, database, lookup

from dateutil import parser as du_pr

from pathlib import Path

db = database()

TZ=pytz.timezone('US/Central')
chi_town = lookup('Chicago', db)
print(chi_town)


rev = "6"

input_dir = '/mnt/d/DivvyDatasets'
input_divvy_basename = "divvy_trip_history_201909-202108"
input_divvy_base = input_dir + "/" + input_divvy_basename
input_divvy_raw = input_divvy_base + ".csv"
input_divvy_rev = input_dir + "/rev" + rev + "-" + input_divvy_basename + ".csv"
input_chitemp = input_dir + "/" + "ChicagoTemperature.csv"
input_factors = input_dir + "/" + "daily_rides_and_factors.csv"

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




def update_start_cat_to_category(df):
  cats = ['AM_EARLY', 'AM_RUSH', 'AM_MID',
            'LUNCH',
            'PM_EARLY', 'PM_RUSH', 'PM_EVENING', 'PM_LATE']

  cats_type = pt.CategoricalDtype(categories=cats, ordered=True)
  df['start_cat'] = df['start_cat'].astype(cats_type)

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
    'total_solar_radiation': int,
    'is_dark': bool
    }
  types_dict.update({col: str for col in col_names if col not in types_dict})

  date_cols=['started_at','ended_at','date']

  df = pd.read_csv(filename, dtype=types_dict,
                   parse_dates=date_cols)

  if 'start_time' in df:
    print("Converting start_time")
    df['start_time'] = df['start_time'].apply(lambda x: dt.datetime.strptime(x, "%H:%M:%S"))

  return df



def yrmo(year, month):
    return "{}-{}".format(year, month)




def calc_duration_in_minutes(started_at, ended_at):
    diff = ended_at - started_at
    return diff.total_seconds() / 60




#
# load the chicago temperature into a data frame
#
def load_temperature_dataframe():
  print("Loading " + input_chitemp)

  date_cols=['date']
  df = pd.read_csv(input_chitemp,
                   parse_dates=date_cols)


  return df




#
# load the chicago temperature into a data frame
#
def load_factors_dataframe():
  print("Loading " + input_factors)

  date_cols=['date']
  df = pd.read_csv(input_factors,
                    parse_dates=date_cols)

#  print("Converting date")
#  df['date'] = df['date'].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"))

  return df



def add_start_time(started_at):
    return started_at.time()




def add_start_cat(started_at):
  start_time = started_at.time()
  time_new_day = dt.time(00,00)
  time_am_rush_start = dt.time(7,00)
  time_am_rush_end = dt.time(9,00)

  time_lunch_start = dt.time(11,30)
  time_lunch_end = dt.time(13,00)

  time_pm_rush_start = dt.time(16,30)
  time_pm_rush_end = dt.time(19,00)

  time_evening_end = dt.time(23,00)


  if start_time >= time_new_day and start_time < time_am_rush_start:
    return 'AM_EARLY'

  if start_time >= time_am_rush_start and start_time < time_am_rush_end:
    return 'AM_RUSH'

  if start_time >= time_am_rush_end and start_time < time_lunch_start:
    return 'AM_MID'

  if start_time >= time_lunch_start and start_time < time_lunch_end:
    return 'LUNCH'

  # slight change on Chi rush from 15:00 to 15:30
  if start_time >= time_lunch_end and start_time < time_pm_rush_start:
    return 'PM_EARLY'

  if start_time >= time_pm_rush_start and start_time < time_pm_rush_end:
    return 'PM_RUSH'

  if start_time >= time_pm_rush_end and start_time < time_evening_end:
    return 'PM_EVENING'

  return 'PM_LATE'




def add_is_dark(started_at):
  st = started_at.replace(tzinfo=TZ)
  chk = sun(chi_town.observer, date=st, tzinfo=chi_town.timezone)
  return st >= chk['dusk'] or st <= chk['dawn']




#
# handles loading and processing the divvy raw data by
#   adding columns, removing bad data, etc.
#
def process_raw_divvy(filename):
  df_divvy = load_divvy_dataframe(filename)

  print("Creating additional columns")
  data = pd.Series(df_divvy.apply(lambda x: [
                    add_start_time(x['started_at']),
                    add_is_dark(x['started_at']),
                    yrmo(x['year'], x['month']),
                    calc_duration_in_minutes(x['started_at'], x['ended_at']),
                    add_start_cat(x['started_at'])
                  ], axis = 1))

  print("Creating temp dataframe")
  new_df = pd.DataFrame(data.tolist(),
                        data.index, 
                        columns=['start_time','is_dark','yrmo','duration','start_cat'])

  print("Merging columns to divy dataframe")
  df_divvy = df_divvy.merge(new_df, left_index=True, right_index=True)

  #
  # add the temperature
  #
  df_chitemp = load_temperature_dataframe()

  print("Merging in temperature")
  df_divvy = pd.merge(df_divvy, df_chitemp, on="date")
  print(df_divvy.shape)
  print(df_divvy.head())

  print("Merging in factors/events")
  df_factors = load_factors_dataframe()
  df_divvy = pd.merge(df_divvy, df_factors, on="date")
  print(df_divvy.shape)

  #
  # clean the dataframe to remove invalid durations
  #   which are really only (about) < 1 minute, or > 12 hours
  #
  print("Removing invalid durations")
  df_divvy = df_divvy[(df_divvy.duration >= 1.2) & (df_divvy.duration < 60 * 12)]
  # print(df_divvy.shape)

  df_divvy = update_dow_to_category(df_divvy)
  df_divvy = update_start_cat_to_category(df_divvy)

  #
  # drop some bogus columns
  #
  print("Dropping columns")
  df_divvy.drop(df_divvy.columns[[0,-1]], axis=1, inplace=True)

  return df_divvy




#
# writes the dataframe to the specified filename
#
def save_dataframe(df, filename):
  print("Saving dataframe to " + filename)
  df_out = df.copy()
  df_out['date'] = df_out['date'].map(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
  df_out.to_csv(filename, index=False, date_format="%Y-%m-%d %H:%M:%S")


#
# load the divvy csv into a data frame
#


if rev_file_exists():
  df_divvy = load_divvy_dataframe(input_divvy_rev)
  df_divvy = update_dow_to_category(df_divvy)
  df_divvy = update_start_cat_to_category(df_divvy)
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





