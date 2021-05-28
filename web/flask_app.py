import time

from flask import Flask, request, jsonify, render_template, redirect
import joblib
import traceback
import pandas as pd

from conf.settings import FLASK_PORT
from src.models.residences import Residences
from web.crawl_item import crawl_item

app = Flask(__name__)
app.debug = True

lr = joblib.load('./web/randomfs.pkl')
print ('Model loaded')
rnd_columns = joblib.load('./web/rnd_columns.pkl')

print ('Model columns loaded')

@app.route('/')
def home():
    return redirect('/predict', code=302)


@app.route('/prediction-api', methods=['POST'])
def predict_api():
    if lr:
        try:
            json_ = request.json
            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=rnd_columns, fill_value=0)

            predict = list(lr.predict(query))

            return jsonify({'prediction': str(predict)})
        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Model is not good')
        return 'Model is not good'


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    res_table = Residences()
    zones = res_table.get_zones()

    if request.method == 'POST':

        if request.form.get('url_to_crawl'):
            item = None
            item = crawl_item(request.form.get('url_to_crawl'))

            total_sleep = 0
            while item is None:
                print('Crawler iteration - waiting for item in flask - sleep 0.5')
                total_sleep += 0.5
                time.sleep(0.5)
                if total_sleep == 8:
                    return render_template("layout.html", zones=zones, error_msg='Nu am putut face extrage detaliile despre apartament')

            # print('Item:', item)
            if 'error' in item:
                return render_template("layout.html", zones=zones, error_msg=item.get('error'))
            json_ = item
        else:
            json_ = {}

            for key, val in request.form.items(multi=False):
                if val:
                    json_[key] = float(val)

        json_= [json_]

        print('Json:', json_)

        query = pd.get_dummies(pd.DataFrame(json_))
        query = query.reindex(columns=rnd_columns, fill_value=0)

        predict = list(lr.predict(query))

        print('Prediction:', predict)

        price_range_min = round(predict[0]) * 50
        price_range_max = round(predict[0]) * 50 + 50
        string_interval = "{} - {}".format(price_range_min, price_range_max)

        value = None
        if json_[0].get('price'):
            if price_range_min > json_[0].get('price'):
                value = 'subevaluat'
            elif price_range_max < json_[0].get('price'):
                value = 'supraevaluat'
            else:
                value = 'evaluat corect'
        return render_template("layout.html", zones=zones, price_interval=string_interval,
                               specs=translate_specs(json_[0]), value=value)
    else:
        return render_template("layout.html", zones=zones)


def translate_specs(raw_json):
    json = {
        "Suprafața construită(mp2)": raw_json.get('built_area', '-999'),
        "Suprafața utilă(mp2)": raw_json.get('livable_area', '-999'),
        "Nr. camere": raw_json.get('rooms', '-999'),
        "Balcoane": raw_json.get('balconies', '-999'),
        "Balcoane închise": raw_json.get('balconies_closed', '-999'),
        "Nr. băi": raw_json.get('bathrooms', '-999'),
        "Comfort": raw_json.get('comfort', '-999'),
        "Etaj": raw_json.get('floor', '-999'),
        "Număr etaje": raw_json.get('floors', '-999'),
        "Anul clădirii": raw_json.get('building_year', '-999'),
        "Tip apartament": raw_json.get('layout', '-999'),
        "Id zona": raw_json.get('zone_id', '-999'),
        "Preț chirie": raw_json.get('price', '-999')
    }



    return {k: v for k, v in json.items() if v and '-999' not in str(v)}



# if __name__ == '__main__':
#     port = FLASK_PORT
#
#     lr = joblib.load('randomfs.pkl')
#     print ('Model loaded')
#     rnd_columns = joblib.load('rnd_columns.pkl')
#
#     print ('Model columns loaded')
#
#     app.run(port=port)


"""
body

[{
    "balconies": 1,
    "balconies_closed": 1,
    "bathrooms": 2,
    "built_area": 78,
    "livable_area": 70,
    "comfort": 1,
    "floor": 5,
    "floors": 10,
    "layout": 1,
    "rooms": 2,
    "zone_id": 5,
    "building_year": 1960
}]
"""