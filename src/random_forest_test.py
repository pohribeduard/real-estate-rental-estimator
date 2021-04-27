from datetime import datetime

import numpy as np
import math
from src.models.residences import Residences
import pandas as pd

from src.visualization.feature_importance import print_feature_importance

residences_nr = 120000

list_features_to_drop = ['price', 'currency', 'price_interval']

residence_table = Residences()
residences = residence_table.get_residences(residences_nr)
# residences = residence_table.get_all_residences()
print('Number of residences: {}'.format(len(residences)))
residences = pd.DataFrame(residences)
residences = residences.fillna(-999)
residences = residences.sample(frac=1)

# target = np.array(residences['price'])
target = np.array(residences['price_interval'])
features = residences.drop(list_features_to_drop, axis=1)
features_columns = features.columns
feature_list = list(features.columns)
features = np.array(features)

data_train = features[:math.floor(len(features) * 0.9)]
target_train = target[:math.floor(len(target) * 0.9)]
print('Number of training samples: {}'.format(len(data_train)))

data_test = features[math.floor(len(features) * 0.9):]
target_test = target[math.floor(len(target) * 0.9):]
print('Number of test samples: {}'.format(len(data_test)))

## RANDOM FOREST - MODEL

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=1400,
                           min_samples_split=2,
                           min_samples_leaf=2,
                           max_features='auto',
                           random_state=42,
                           max_depth=70,
                           criterion='mse',
                           bootstrap=True,
                           verbose=1,
                           n_jobs=-1)

print('Training model on {} samples'.format(len(data_train)))

rf.fit(data_train, target_train)

print('Predicting {} prices'.format(len(data_test)))

predictions = rf.predict(data_test)

errors = abs(predictions - target_test)

print('Mean Absolute Error:', round(np.mean(errors), 2))

mape = 100 * (errors / target_test)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

print('\n \n Predictions samples:')
for i in range(min(len(predictions), 30)):
    print('Predicted: {},        Actual: {},        Predicted interval: {},        Actual interval: {}'.format(
        predictions[i], target_test[i], round(predictions[i]), round(target_test[i])))

total_accurate = 0
for i in range(len(predictions)):
    if round(predictions[i]) == round(target_test[i]):
        total_accurate += 1
        # print(predictions[i])
        # print(target_test[i])

print('\nTotal accurate price intervals: {}/{}'.format(total_accurate, len(predictions)))

print_feature_importance(rf, feature_list)

# Serialize the model and save
#
#
import joblib

# now = datetime.now().strftime('%m-%d-%Y_%H_%M_%S')
# err = str(round(np.mean(errors), 2)).replace('.', '-')
#
# joblib.dump(rf, '../saved_models/randomfs_{}_{}_{}.pkl'.format(total_accurate, err, now))
# print("Random Forest Model Saved")
# #Load the model
# lr = joblib.load('../saved_models/randomfs_{}_{}_{}.pkl'.format(total_accurate, err, now))
# # Save features from training
# rnd_columns = list(features_columns)
# joblib.dump(rnd_columns, '../saved_models/rnd_columns_{}_{}_{}.pkl'.format(total_accurate, err, now))
# print("Random Forest Model Colums Saved")
