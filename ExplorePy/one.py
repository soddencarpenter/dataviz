import pandas as pd
import numpy as np

data = np.array(['python','php','java'])
series = pd.Series(data)
print (series)

# Create a Dict from a input
data = {'Courses' :"pandas", 'Fees' : 20000, 'Duration' : "30days"}
s2 = pd.Series(data)
print (s2)


# read the chicago temperature csv into a data frame
#  in python, starts with column 0
chitemp = pd.read_csv('/mnt/d/DivvyDatasets/ChicagoTemperature.csv')
print(chitemp)

# some info on the chitemp dataframe
print(chitemp.shape)  # rows, cols as a tuple, e.g. (731, 9)
print(chitemp.columns.values) # the column names as a list
print(chitemp['avg_temperature_fahrenheit']) # the values of the column

# create a new dataframe for when temperature >. 80
chihot = chitemp[chitemp['avg_temperature_fahrenheit'] >= 80.0]
print(chihot)


def is_hot(temp):
    if temp >= 80.0:
        return True
    else:
        return False

# add a new column to the chitemp indicating if it is hot
#  column is added by using a function
chitemp['ishot'] = chitemp['avg_temperature_fahrenheit'].apply(is_hot)
print(chitemp)