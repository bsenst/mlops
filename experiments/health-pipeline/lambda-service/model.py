# https://github.com/DataTalksClub/mlops-zoomcamp/blob/997bbf7172d0e36b1f86ef11c4c9b359e452dbb4/06-best-practices/code/model.py

import os
import json
import base64

import boto3
import mlflow
import pickle
from sklearn.linear_model import LogisticRegression

def get_model_location(run_id):
    model_location = os.getenv('MODEL_LOCATION')

    if model_location is not None:
        return model_location

    model_bucket = os.getenv('MODEL_BUCKET', 's3bucket')
    experiment_id = os.getenv('MLFLOW_EXPERIMENT_ID', '1')

    model_location = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts/model'
    return model_location

def load_model(run_id):
    model_path = get_model_location(run_id)
    model = mlflow.pyfunc.load_model(model_path)
    return model

class ModelService:

    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def predict(self, features):
        pred = self.model.predict(features)
        return pred[0]
                     
    def handler_name(event, context):

        # prepare features
        age = int(event["age"])
        gender = int(event["gender"]=="female")
        sbp = int(event["sbp"])
        glc = int(int(event["glc"])>120)
        chol = int(event["chol"])

        predictions_events = []

        prediction = self.predict([[age, gender, sbp, glc, chol]])

        prediction_event = {
            'model': 'heart_disease_prediction_model',
            'version': self.model_version,
            'prediction': {'heart disease': prediction},
        }

        for callback in self.callbacks:
            callback(prediction_event)

        predictions_events.append(prediction_event)

        return {'predictions': predictions_events}

class KinesisCallback:
    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        ride_id = prediction_event['prediction']['ride_id']

        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(ride_id),
        )

def create_kinesis_client():
    endpoint_url = "http://127.0.0.1:4566"

    if endpoint_url is None:
        return boto3.client('kinesis')

    return boto3.client('kinesis', endpoint_url=endpoint_url)

def init(prediction_stream_name: str, run_id: str, test_run: bool):
    model = load_model(run_id)

    callbacks = []

    if not test_run:
        kinesis_client = create_kinesis_client()
        kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service