import numpy as np
import math
from src.models.residences import Residences
import pandas as pd

test_nr = 10
residences_nr = 150

list_features_to_drop = ['price', 'currency']

residence_table = Residences()
residences = residence_table.get_residences(residences_nr)
residences = pd.DataFrame(residences)
residences = residences.fillna(-1)
residences = residences.sample(frac=1)

target = np.array(residences['price'])
features = residences.drop(list_features_to_drop, axis=1)
feature_list = list(features.columns)
features = np.array(features)


data_train = features[:math.floor(len(features) * 0.8)]
target_train = target[:math.floor(len(target) * 0.8)]

data_test = features[math.floor(len(features) * 0.8):]
target_test = target[math.floor(len(target) * 0.8):]

## RANDOM FOREST - MODEL

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=1400,
                               min_samples_split=5,
                               min_samples_leaf=2,
                               max_features='sqrt',
                               random_state=42,
                               max_depth=None,
                               criterion='mse',
                               bootstrap=False,
                               verbose=1)

rf.fit(data_train, target_train)

predictions = rf.predict(data_test)

errors = abs(predictions - target_test)

print('Mean Absolute Error:', round(np.mean(errors), 2))

mape = 100 * (errors / target_test)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')




# y = rf.feature_importances_
# list_y = [a for a in y if a > 0.005]
# print(list_y)
#
# list_of_index = []
# for i in list_y:
#     a = np.where(y==i)[0][0]
#     list_of_index.append(a)
# print(list_of_index)
#
# col = []
# for i in feature_list:
#     col.append(i)
# labels = []
#
# for i in list_of_index:
#     b = col[i]
#     labels.append(b)
#
#
# import matplotlib.pyplot as plt
# y = list_y
# fig, ax = plt.subplots()
# width = 0.8
# ind = np.arange(len(y))
# ax.barh(ind, y,width, color="pink")
# ax.set_yticks(ind+width/10)
# ax.set_yticklabels(labels, minor=False)
# plt.title('Feature importance in Random Forest Regression')
# plt.xlabel('Relative importance')
# plt.ylabel('feature')
# plt.figure(figsize=(10,8.5))
# fig.set_size_inches(10, 8.5, forward=True)
# plt.show()


