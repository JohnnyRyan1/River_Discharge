#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Download ERA5 data the Copernicus Climate Change Service API (https://cds.climate.copernicus.eu/)

You can go to: https://cds.climate.copernicus.eu/cdsapp#!/yourrequests
to check the progress of your request.

"""

# Get your UID and API key from https://cds.climate.copernicus.eu/user and insert it in the variables below
UID = '20018'
API_key = '178524fd-b8ed-4702-be62-ad1797c7a002'

# Write the keys into the file ~/.cdsapirc in the home directory of your user
import os
with open(os.path.join(os.path.expanduser('~'), '.cdsapirc'), 'w') as f:
    f.write('url: https://cds.climate.copernicus.eu/api/v2\n')
    f.write(f'key: {UID}:{API_key}')

# Define destination to save
dest = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/era/'
    
# Start a request
# You will be asked to agree to the terms of use from the copernicus climate data store for your first download.

# Import cdsapi and create a Client instance
import cdsapi
c = cdsapi.Client()

# ERA5-land request
c.retrieve(
    'reanalysis-era5-land',
    {
        'format': 'netcdf',
        'variable': [
            '2m_temperature', 'runoff', 'snow_depth_water_equivalent',
            'snowmelt', 'total_evaporation', 'total_precipitation',
            'volumetric_soil_water_layer_1',
        ],
        'area': [
            43.4, -124.1, 40.1,
            -120.5,
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'year': '2019',
    },
    dest + 'variables_2019.nc')

# Alternative request for ERA5 standard reanalysis product
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            '2m_temperature', 'mean_evaporation_rate', 'mean_runoff_rate',
            'mean_snowmelt_rate', 'mean_total_precipitation_rate', 'snow_depth',
            'volumetric_soil_water_layer_1',
        ],
        'year': '2019',
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'area': [
            43.4, -124.1, 40.1,
            -120.5,
        ],
        'format': 'netcdf',
    },
     dest + 'variables_2019.nc')