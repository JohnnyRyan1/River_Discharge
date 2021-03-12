#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Apply model to another year.

"""

# Import modules
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler  
import matplotlib.pyplot as plt
import pickle

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/'

###############################################################################
# Define constants
###############################################################################

# Define coordinate system
df_crs = 'EPSG:4326'

# Load models
rf_model = pickle.load(open(filepath + '/models/klamath_rf.sav', 'rb'))
nn_model = pickle.load(open(filepath + '/models/klamath_nn.sav', 'rb'))

# Import discharge data
label_data = pd.read_csv(filepath + 'data/discharge/Klamath_Discharge_Daily_2020.csv')

###############################################################################
# Import climate data
###############################################################################

climate_2019 = pd.read_csv(filepath + 'data/era/era5_training_data_2019.csv')
climate_2020 = pd.read_csv(filepath + 'data/era/era5_training_data_2020.csv')

###############################################################################
# Prepare data
###############################################################################

# Define feature list
feature_list = ['t2m', 'mer', 'mtpr', 'swvl1', 'msmr', 'sd', 'sd_diff', 'mtpr_1days',
                'mtpr_2days', 'mtpr_3days', 'mtpr_4days', 'mtpr_5days', 'mtpr_6days', 
                'mtpr_7days', 'msmr_1days', 'msmr_2days', 'msmr_3days', 'msmr_4days', 
                'msmr_5days', 'msmr_6days', 'msmr_7days']

# Define labels and targets (note that we can't use all data because of some NaNs at the start)
X = climate_2020[feature_list][7:]

# Standarize data (not necessary for Random Forests but it is for other algorithms)
scaler = StandardScaler()  
X_scaled = scaler.fit(X).transform(X)

###############################################################################
# Perform machine learning using Neural Network and Random Forests
###############################################################################

# Predict
predictions_nn = nn_model.predict(X_scaled)
predictions_rf = rf_model.predict(X_scaled)

###############################################################################
# Evaluate predictions
###############################################################################

# Calculate the absolute errors
errors = abs(predictions_rf - label_data['discharge'][7:])

# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 3))

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / label_data['discharge'][7:])

# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

plt.plot(predictions_rf)
plt.plot(predictions_nn)
plt.plot(label_data['discharge'])

# Calculate Nash-Sutcliffe Efficiency 
nse = 1 - (np.sum((label_data['discharge'] - label_data['predictions'])**2) / 
           np.sum((label_data['discharge'] - np.mean(label_data['discharge']))**2))























