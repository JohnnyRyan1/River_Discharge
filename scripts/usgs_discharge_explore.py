#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Klamath discharge format from USGS.

Data can be downloaded at:
https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00060=on&format=rdb&site_no=11530500&period=&begin_date=2018-09-01&end_date=2020-09-01

"""

# Import modules
import pandas as pd
import matplotlib.pyplot as plt

# Define filename
filename = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/Klamath_Discharge_2018_2020.txt'

# Read data
df = pd.read_csv(filename, skiprows=28, sep='\t', parse_dates=[2])

# Set columns names
df.columns = ['agency', 'site_no', 'datetime', 'time_zone', 'discharge', 'status']

# Save as csv
df.to_csv('/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/Klamath_Discharge_2018_2020.csv')

# Plot discharge
plt.plot(df['datetime'], df['discharge'])






