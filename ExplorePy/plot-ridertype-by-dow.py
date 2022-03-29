#
# assumes df_divvy is loaded and corrected
#

import pandas as pd
import numpy as np
import datetime as datetime
import matplotlib.pyplot as pyplot
import pandas.api.types as pt
import seaborn as sns



#
# average ride type by rider & day of week
#
df_rider_by_dow = df_divvy.groupby(['member_casual','day_of_week']).agg(mean_time = ('duration', 'mean')).round(2)
df_rider_by_dow.sort_values(by=['member_casual','day_of_week'])
print(df_rider_by_dow)

# this uses the standard plot
df_rider_by_dow.unstack('member_casual').plot(kind='bar')


# this uses seaborn
df_rider_by_dow.reset_index(inplace=True)
sns.set(rc={"figure.figsize":(16,8)})
sns.barplot(data=df_rider_by_dow, x="day_of_week", y="num_rides", hue="member_casual")