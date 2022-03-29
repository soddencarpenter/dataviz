import pandas as pd
import numpy as np
import datetime as datetime
import pandas.api.types as pt



input_dir = '/mnt/d/DivvyDatasets'
input_divvy = input_dir + "/" + "divvy_trip_history_201909-202108.csv"
input_chitemp = input_dir + "/" + "ChicagoTemperature.csv"


def yrmo(year, month):
    return "{}-{}".format(year, month)


def calc_duration_in_minutes(started_at, ended_at):
    st = datetime.datetime.strptime(started_at, '%Y-%m-%d %H:%M:%S')
    en = datetime.datetime.strptime(ended_at, '%Y-%m-%d %H:%M:%S')
    diff = en - st
    return diff.total_seconds() / 60

#
# load the divvy csv into a data frame
#
print("Loading " + input_divvy)
# so need to set the type on a couple of columns
col_names = pd.read_csv(input_divvy, nrows=0).columns
types_dict = { 'ride_id': str, 
  'start_station_id': str,
  'end_station_id': str}
types_dict.update({col: str for col in col_names if col not in types_dict})
df_divvy = pd.read_csv(input_divvy, dtype=types_dict)
print(df_divvy)


#
# load the chicago temperature into a data frame
#
print("Loading " + input_chitemp)
df_chitemp = pd.read_csv(input_chitemp)
print(df_chitemp)


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
# btw, can just pass the row and let the function figure it out
#
#def procone(row):
#    print(row['date'])
#    return 0
#df_divvy.apply(lambda row: procone(row), axis = 1)



#
# add the temperature
#
print("Merging in temperature")
df_divvy = pd.merge(df_divvy, df_chitemp,
  on="date")
print(df_divvy.shape)
print(df_divvy.head())
print(df_divvy.loc[df_divvy['date'] == '2020-02-21'])

print(df_divvy.info())  # shows mem usage, other info
print(df_divvy[['ride_id','member_casual','date','duration','yrmo','avg_temperature_fahrenheit']])


#
# clean the dataframe to remove invalid durations
#   which are really only (about) < 1 minute, or > 12 hours
#
print("Removing invalid durations")
df_divvy = df_divvy[(df_divvy.duration >= 1.2) & (df_divvy.duration < 60 * 12)]
print(df_divvy.shape)


#
# we need to get the dow properly set
#
cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

cats_type = pt.CategoricalDtype(categories=cats, ordered=True)
df_divvy['day_of_week'] = df_divvy['day_of_week'].astype(cats_type)
