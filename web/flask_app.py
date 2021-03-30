from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd

from conf.settings import FLASK_PORT

app = Flask(__name__)


@app.route('/prediction', methods=['POST'])
def predict():
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

if __name__ == '__main__':
    port = FLASK_PORT

    lr = joblib.load('randomfs.pkl')
    print ('Model loaded')
    rnd_columns = joblib.load('rnd_columns.pkl')
    print ('Model columns loaded')
    app.run(port=port, debug=True)