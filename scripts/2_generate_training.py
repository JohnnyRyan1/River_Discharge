#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Generate training data from ERA5.

"""

# Import modules
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
from shapely.geometry import Point

###############################################################################
# Define constants
###############################################################################

# Define coordinate system
df_crs = 'EPSG:4326'

year = '2019'

###############################################################################
# Read data
###############################################################################

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge_Prediction/data/'

# Import Klamath Basin shapefile
basin = gpd.read_file(filepath + 'basin/klamath_basin_lev05.shp')
basin = basin.set_crs(df_crs)

# Import ERA5 data, 'ds' is dataset
ds = xr.open_dataset(filepath + 'era/era5_reanalysis_' + year + '.nc')

###############################################################################
# Clip ERA5 grid with shapefile
###############################################################################
# Get array of all lat lons
xx, yy = np.meshgrid(ds['longitude'].values, ds['latitude'].values)

# Convert to DataFrame to get lat lons
df = pd.DataFrame({'lon':np.ravel(xx), 'lat':np.ravel(yy)})

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, crs=df_crs, geometry=geometry)

# Spatial join of ERA5 grid points within Klamath Basin shapefile
merged = gpd.tools.sjoin(gdf, basin, op='within')

# Define target latitude and longitude
indices = np.unravel_index(merged.index, (14,15))
target_lon = xr.DataArray(merged['lon'].values, dims="points")
target_lat = xr.DataArray(merged['lat'].values, dims="points")

# Mask ERA5 grid
ds_masked = ds.sel(longitude=target_lon, latitude=target_lat, method="nearest")

###############################################################################
# Spatial average and resample to daily
###############################################################################

# Get spatial averages
ds_mean = np.mean(ds_masked, axis=(1))

# Convert to DataFrame and add datetime column
final_df = ds_mean.to_dataframe()
final_df['datetime'] = ds_masked['time']
final_df.set_index('datetime', inplace=True)

# Resample to daily
final_df_daily = final_df.resample('D').mean()

###############################################################################
# Basic feature engineering
###############################################################################

# Compute Snow depth change
final_df_daily['sd_diff'] = final_df_daily['sd'].diff()

# Convert snow accumulation (i.e. snow depth change > 0) to zeros since we only want a proxy for melt
final_df_daily['sd_diff'][final_df_daily['sd_diff'] > 0] = 0

# Compute time-lagged precipitation
for i in np.arange(1, 8, 1):
    final_df_daily['mtpr_'+ str(i) + 'days'] = final_df_daily['mtpr'].shift(periods=i)
    
# Compute time-lagged snow melt
for i in np.arange(1, 8, 1):
    final_df_daily['msmr_'+ str(i) + 'days'] = final_df_daily['msmr'].shift(periods=i)
    
# Compute snow-on or snow-off boolean
final_df_daily['msmr_'+ str(i) + 'days'] = final_df_daily['msmr'].shift(periods=i)

###############################################################################
# More advanced feature engineering
###############################################################################

# Compute time-lagged precipitation with aggregation
final_df_daily['mtpr'].shift(periods=3).rolling(3).sum() / 3

# Spatial weighting?

###############################################################################
# Save to csv
###############################################################################

final_df_daily.to_csv(filepath + 'era/era5_training_data_' + year + '.csv')








