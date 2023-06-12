#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import sklearn

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

df = read_data('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-04.parquet')

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

# Q2. Preparing the output
year = 2022
month = 4

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

df_results = pd.DataFrame()
df_results['ride_id'] = df['ride_id']
df_results['y_pred'] = y_pred

print(df_results['y_pred'].mean())

df_results.to_parquet(
    "df_results.parquet",
    engine='pyarrow',
    compression=None,
    index=False
)
