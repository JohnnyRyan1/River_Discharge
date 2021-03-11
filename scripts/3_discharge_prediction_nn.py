#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Predict Klamath River discharge using Neural Network.

"""

# Import modules
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  
import matplotlib.pyplot as plt

###############################################################################
# Import data
###############################################################################

# Define filepath
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/River_Discharge/data/'

# Import data
training_data = pd.read_csv(filepath + 'era/era5_training_data.csv')
label_data = pd.read_csv(filepath + 'discharge/Klamath_Discharge_Daily_2019.csv')

###############################################################################
# Prepare data
###############################################################################

# Define feature list
feature_list = ['t2m', 'mer', 'mtpr', 'swvl1', 'msmr', 'sd', 'sd_diff', 'mtpr_1days',
                'mtpr_2days', 'mtpr_3days', 'mtpr_4days', 'mtpr_5days', 'mtpr_6days', 
                'mtpr_7days', 'msmr_1days', 'msmr_2days', 'msmr_3days', 'msmr_4days', 
                'msmr_5days', 'msmr_6days', 'msmr_7days']

# Define labels and targets (note that we can't use all data because of some NaNs at the start)
label_data = label_data[8:]
training_data = training_data[8:]
y = label_data['discharge']
X = training_data[feature_list]

# Standarize data (not necessary for Random Forests but it is for other algorithms)
scaler = StandardScaler()  
X_scaled = scaler.fit(X).transform(X)

###############################################################################
# Perform machine learning  using Neural Network
###############################################################################

# Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define classifier
classifier = MLPRegressor(solver='adam', alpha=0.05, hidden_layer_sizes=(100,), 
                          random_state=1, max_iter=100000)

# Train classifier
classifier.fit(X_train, y_train)

# Predict
predictions = classifier.predict(X_test)

###############################################################################
# Evaluate model
###############################################################################

# Calculate the absolute errors
errors = abs(predictions - y_test)

# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 3))

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / y_test)

# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

###############################################################################
# Apply model to entire discharge record and vizualize predictions
###############################################################################

# Make predictions
predictions = classifier.predict(X_scaled)

# Add to original DataFrame
label_data['predictions'] = predictions
                
# Plot
plt.plot(label_data['discharge'])
plt.plot(label_data['predictions'])

# Calculate Nash-Sutcliffe Efficiency 
nse = 1 - (np.sum((label_data['discharge'] - label_data['predictions'])**2) / 
           np.sum((label_data['discharge'] - np.mean(label_data['discharge']))**2))




















