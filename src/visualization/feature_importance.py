import numpy as np
import matplotlib.pyplot as plt

def print_feature_importance(rf, feature_list):
    y = rf.feature_importances_
    list_y = [a for a in y if a > 0.005]
    # print(list_y)

    list_of_index = []
    for i in list_y:
        a = np.where(y == i)[0][0]
        list_of_index.append(a)
    # print(list_of_index)

    col = []
    for i in feature_list:
        col.append(i)
    labels = []

    for i in list_of_index:
        b = col[i]
        labels.append(b)

    y = list_y
    fig, ax = plt.subplots()
    width = 0.8
    ind = np.arange(len(y))
    ax.barh(ind, y, width, color="pink")
    ax.set_yticks(ind + width / 10)
    ax.set_yticklabels(labels, minor=False)
    plt.title('Feature importance in Random Forest Regression')
    plt.xlabel('Relative importance')
    plt.ylabel('feature')
    plt.figure(figsize=(10, 8.5))
    fig.set_size_inches(10, 8.5, forward=True)
    plt.show()
