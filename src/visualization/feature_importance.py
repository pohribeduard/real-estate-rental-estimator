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
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    width = 0.8
    ind = np.arange(len(y))
    ax.barh(ind, y, width, color="#3498DB")
    ax.set_yticks(ind + width / 10)
    ax.set_yticklabels(tr_labels(labels), minor=False)
    plt.title('Importanța caracteristicilor în antrenarea modelului')
    plt.xlabel('Importanța')
    plt.ylabel('Caracteristica')
    plt.figure(figsize=(10, 8.5))
    fig.set_size_inches(10, 8.5, forward=True)
    plt.show()

def tr_labels(labels):
    translated_labels = []
    for l in labels:
        if 'balconies' in l:
            l = 'Nr. balcoane'
            translated_labels.append(l)
        elif 'balconies_closed' in l:
            l = 'Nr. balcoane închise'
            translated_labels.append(l)
        elif 'bathrooms' in l:
            l = 'Nr. băi'
            translated_labels.append(l)
        elif 'built_area' in l:
            l = 'Suprafață construită'
            translated_labels.append(l)
        elif 'livable_area' in l:
            l = 'Suprafață utilă'
            translated_labels.append(l)
        elif 'comfort' in l:
            l = 'Comfort'
            translated_labels.append(l)
        elif 'floors' in l:
            l = 'Nr. etaje'
            translated_labels.append(l)
        elif 'floor' in l:
            l = 'Etaj'
            translated_labels.append(l)
        elif 'furnished' in l:
            l = 'Mobilat'
            translated_labels.append(l)
        elif 'layout' in l:
            l = 'Tip'
            translated_labels.append(l)
        elif 'rooms' in l:
            l = 'Nr. camere'
            translated_labels.append(l)
        elif 'zone_id' in l:
            l = 'Zona'
            translated_labels.append(l)
        elif 'building_year' in l:
            l = 'Anul clădirii'
            translated_labels.append(l)

    return translated_labels

