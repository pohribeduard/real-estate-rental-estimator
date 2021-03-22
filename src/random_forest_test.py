import numpy as np
import math
from src.models.residences import Residences
import pandas as pd

from src.visualization.feature_importance import print_feature_importance

residences_nr = 1200

list_features_to_drop = ['price', 'currency', 'price_interval']

residence_table = Residences()
residences = residence_table.get_residences(residences_nr)
# residences = residence_table.get_all_residences()
residences = pd.DataFrame(residences)
residences = residences.fillna(-999)
residences = residences.sample(frac=1)

target = np.array(residences['price_interval'])
features = residences.drop(list_features_to_drop, axis=1)
features_columns = features.columns
feature_list = list(features.columns)
features = np.array(features)


data_train = features[:math.floor(len(features) * 0.85)]
target_train = target[:math.floor(len(target) * 0.85)]

data_test = features[math.floor(len(features) * 0.85):]
target_test = target[math.floor(len(target) * 0.85):]

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
                           n_jobs=3)

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
    print('Predicted: {},      Actual: {}'.format(predictions[i], target_test[i]))

total_accurate = 0
for i in range(min(len(predictions), 30)):
    if round(predictions[i]) == target_test[i]:
        total_accurate += 1

print('\n Total accurate price intervals: {}/{}'.format(total_accurate, len(predictions)))

print_feature_importance(rf, feature_list)


#Serialize the model and save


import joblib

joblib.dump(rf, 'randomfs.pkl')
print("Random Forest Model Saved")
#Load the model
lr = joblib.load('randomfs.pkl')
# Save features from training
rnd_columns = list(features_columns)
joblib.dump(rnd_columns, 'rnd_columns.pkl')
print("Random Forest Model Colums Saved")


