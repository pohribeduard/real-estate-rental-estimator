import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

from src.models.residences import Residences


def result_visualization(nr_res=10000):
    residence_table = Residences()
    residences = residence_table.get_residences(nr_res)

    residences_df = pd.DataFrame(residences)
    residences_df = residences_df[residences_df.rooms.notnull()]
    residences_df = residences_df[residences_df.livable_area > 0]

    X = residences_df['livable_area'].values
    y = residences_df['price'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

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

    rf.fit(X_train.reshape(-1, 1), y_train.reshape(-1, 1))

    y_pred = rf.predict(X_test.reshape(-1, 1))

    df = pd.DataFrame({'Real Values': y_test.reshape(-1), 'Predicted Values': y_pred.reshape(-1)})

    X_grid = np.arange(min(X), max(X), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    plt.scatter(X_test, y_test, color='red')
    plt.scatter(X_test, y_pred, color='green')
    plt.legend({'predicted': 'red', 'actual': 'blue'})
    plt.title('Random Forest Regression')
    plt.xlabel('Livable Area')
    plt.ylabel('Price')
    plt.show()

    plt.plot(X_grid, rf.predict(X_grid), color='black')
    plt.title('Random Forest Regression')
    plt.xlabel('Livable Area')
    plt.ylabel('Price')
    plt.show()
