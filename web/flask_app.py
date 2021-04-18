from flask import Flask, request, jsonify, render_template
import joblib
import traceback
import pandas as pd

from conf.settings import FLASK_PORT

app = Flask(__name__)
app.debug = True


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
    if request.method == 'POST':

        json_ = {}

        for key, val in request.form.items(multi=False):
            if val:
                json_[key] = float(val)

        json_= [json_]

        print(json_)

        query = pd.get_dummies(pd.DataFrame(json_))
        query = query.reindex(columns=rnd_columns, fill_value=0)

        predict = list(lr.predict(query))

        print(predict)

        price_range_min = round(predict[0]) * 50
        price_range_max = round(predict[0]) * 50 + 50
        string_interval = "{} - {} EURO".format(price_range_min, price_range_max)
        return render_template("layout.html", price_interval=string_interval)
    else:
        return render_template("layout.html")

if __name__ == '__main__':
    port = FLASK_PORT

    lr = joblib.load('randomfs.pkl')
    print ('Model loaded')
    rnd_columns = joblib.load('rnd_columns.pkl')

    print ('Model columns loaded')
    app.run(port=port, debug=True)


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