import os
import sys
import pickle
import pandas as pd

def main(year, month):

    options = {
        'client_kwargs': {
            'endpoint_url': "http://127.0.0.1:4566"
        }
    }

    df = pd.read_parquet('s3://nyc-duration/out/2022-02.parquet', storage_options=options)

    with open('../model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted sum duration:', y_pred.sum())

if __name__ == '__main__':

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    main(year, month)