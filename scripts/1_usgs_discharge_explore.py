#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Import and explore Klamath River discharge from USGS.

Data can be downloaded at:
https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00060=on&format=rdb&site_no=11530500&period=&begin_date=2018-09-01&end_date=2020-09-01

"""

# Import modules
import pandas as pd
import matplotlib.pyplot as plt

# Define filename
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/discharge/'
filename = filepath + 'Klamath_Discharge_2018_2020.txt'

# Read data, 'df' stands for DataFrame
df = pd.read_csv(filename, skiprows=29, sep='\t', parse_dates=[2])

# Set columns names
df.columns = ['agency', 'site_no', 'datetime', 'time_zone', 'discharge', 'status']

# Set datetime as index
df.set_index('datetime', inplace=True)

# Plot discharge
plt.plot(df['discharge'])

# Plot discharge for for December 2018
plt.plot(df['discharge']['2018-12-01':'2018-12-31'])

# Resample to daily and monthly time periods
df_daily = df['discharge'].resample('D').mean()
df_monthly = df['discharge'].resample('M').mean()

# Plot all discharges
plt.plot(df['discharge'])
plt.plot(df_daily)
plt.plot(df_monthly)

# Save as csv
#df_daily.to_csv(filepath + 'Klamath_Discharge_Daily_2018_2020.csv')
df_daily['2018-01-01':'2018-12-31'].to_csv(filepath + 'Klamath_Discharge_Daily_2018.csv')
df_daily['2019-01-01':'2019-12-31'].to_csv(filepath + 'Klamath_Discharge_Daily_2019.csv')
df_daily['2020-01-01':'2020-12-31'].to_csv(filepath + 'Klamath_Discharge_Daily_2020.csv')



