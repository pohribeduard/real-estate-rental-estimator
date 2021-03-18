from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import math
from src.models.residences import Residences

list_features_to_drop = ['price', 'currency']

residence_table = Residences()
residences = residence_table.get_residences(200000)
residences = pd.DataFrame(residences)
residences = residences.fillna(-1)
residences = residences.sample(frac=1)

target = np.array(residences['price'])
features = residences.drop(list_features_to_drop, axis=1)
feature_list = list(features.columns)
features = np.array(features)


# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num = 19)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt', 'log2', None]
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 220, num = 22)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4, 10]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
print(random_grid)

# Use the random grid to search for best hyperparameters
# First create the base model to tune
rf = RandomForestRegressor()
# Random search of parameters, using 3 fold cross validation,
# search across 100 different combinations, and use all available cores
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
rf_random.fit(features, target)

print(rf_random.best_params_)