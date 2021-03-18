import numpy as np

from src.models.residences import Residences
import pandas as pd

list_features_to_drop = ['price', '_sa_instance_state', 'id', 'main_ad_id', 'conditioning',
                         'heating', 'currency', 'availability', 'status', 'created_at']

residence_table = Residences()
residences = residence_table.get_residences(1600)
residences = pd.DataFrame(residences)
residences = residences.fillna(-1)
residences = residences.sample(frac=1)

residences_train = residences[np.math.floor(len(residences) * 0.8):]
residences_test = residences[:np.math.floor(len(residences) * 0.8)]

target_train = np.array(residences_train['price'])
features_train = residences.drop(list_features_to_drop, axis=1)
feature_train_list = list(features_train.columns)
features_train = np.array(features_train)

target_test = np.array(residences_test['price'])
features_test = residences.drop(list_features_to_drop, axis=1)
feature_test_list = list(features_test.columns)
features_test = np.array(features_test)



## RANDOM FOREST - KFOLD AND MODEL


from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer

kf = KFold(n_splits=10, random_state=42, shuffle=True)
accuracies = []

# imp = SimpleImputer(missing_values=np.nan, strategy='mean')
# data_train = imp.fit(data_train)
# target_test = imp.fit(target_test)

rf = RandomForestRegressor(n_estimators=1400,
                           min_samples_split=5,
                           min_samples_leaf=2,
                           max_features='sqrt',
                           random_state=42,
                           max_depth=None,
                           criterion='mse',
                           bootstrap=False,
                           verbose=1)


rf.fit(features_train, target_train)

predictions = rf.predict(features_test)

errors = abs(predictions - target_test)

print('Mean Absolute Error:', round(np.mean(errors), 2))

mape = 100 * (errors / target_test)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

accuracies.append(accuracy)

average_accuracy = np.mean(accuracies)
print('Average accuracy:', average_accuracy)


y = rf.feature_importances_
list_y = [a for a in y if a > 0.005]
print(list_y)

list_of_index = []
for i in list_y:
    a = np.where(y==i)
    list_of_index.append(a)
print(list_of_index)


