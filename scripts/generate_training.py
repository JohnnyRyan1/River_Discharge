#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Generate training data.

"""

# Import modules
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
from shapely.geometry import Point

# Define coordinate system
df_crs = 'EPSG:4326'

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/'

# Import Klamath Basin shapefile
basin = gpd.read_file(filepath + 'basin/klamath_basin_lev05.shp')
basin = basin.set_crs(df_crs)

# Import ERA5 data, 'ds' is dataset
ds = xr.open_dataset(filepath + 'era/era5_reanalysis_2019.nc')

# Get array of all lat lons
xx, yy = np.meshgrid(ds['longitude'].values, ds['latitude'].values)

# Convert to DataFrame to get lat lons
df = pd.DataFrame({'lon':np.ravel(xx), 'lat':np.ravel(yy)})

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, crs=df_crs, geometry=geometry)

# Spatial join of ERA5 grid points within Klamath Basin
merged = gpd.tools.sjoin(gdf, basin, op='within')

# Define target latitude and longitude
indices = np.unravel_index(merged.index, (14,15))
target_lon = xr.DataArray(merged['lon'].values, dims="points")
target_lat = xr.DataArray(merged['lat'].values, dims="points")

# Mask ERA5 grid
ds_masked = ds.sel(longitude=target_lon, latitude=target_lat, method="nearest")

# Get spatial averages
ds_mean = np.mean(ds_masked, axis=(1))

# Convert to DataFrame and add datetime column
final_df = ds_mean.to_dataframe()
final_df['datetime'] = ds_masked['time']
final_df.set_index('datetime', inplace=True)

# Resample to daily



# Export list of points to check in QGIS
df.to_csv('/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/tests/era_grid.csv')
merged.to_csv('/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/tests/basin_grid.csv')








