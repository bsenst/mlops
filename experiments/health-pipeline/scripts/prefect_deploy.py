# https://github.com/bryskulov/mlops-house-prices/blob/70ed118b9dcddb437565f02c274d1eb62e3c3557/model_training/prefect_deploy.py

import pickle

import numpy as np
import pandas as pd
import xgboost as xgb
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from prefect import flow, task
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import mlflow

RANDOM_SEED=42
NUM_BOOST_ROUND=100
EARLY_STOPPING_ROUNDS=10
MAX_EVALS=10

@task
def read_data():
    cleveland = pd.read_csv("./heart-disease/processed.cleveland.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    hungary = pd.read_csv("./heart-disease/processed.hungarian.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    switzerland = pd.read_csv("./heart-disease/processed.switzerland.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    veterans = pd.read_csv("./heart-disease/processed.va.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    heart_disease_df = pd.concat([cleveland, hungary, switzerland, veterans])
    
    return heart_disease_df.sample(int(len(heart_disease_df)*0.8))

@task
def prepare_features(heart_disease_df: pd.DataFrame):
    heart_disease_df = heart_disease_df[["age", "sex", "trestbps", "chol", "fbs", "num"]]
    heart_disease_df.trestbps.replace("?", np.nan, inplace=True)
    heart_disease_df.trestbps.fillna(heart_disease_df.trestbps.astype(float).mean().round(0), inplace=True)
    heart_disease_df["trestbps"] = heart_disease_df.trestbps.astype(int)
    heart_disease_df.chol.replace("?", np.nan, inplace=True)
    heart_disease_df.chol.fillna(heart_disease_df.chol.astype(float).mean().round(0), inplace=True)
    heart_disease_df["chol"] = heart_disease_df["chol"].astype(int)
    heart_disease_df.fbs.replace("?", np.nan, inplace=True)
    heart_disease_df.fbs.fillna(heart_disease_df.fbs.astype(float).mean().round(0), inplace=True)
    heart_disease_df["fbs"] = heart_disease_df["fbs"].astype(int)
    heart_disease_df = heart_disease_df.sample(int(len(heart_disease_df)*0.6)) # simulate changing training data
    X = heart_disease_df.drop('num', axis=1)
    y = heart_disease_df['num']
    return X, y

@task
def split_dataset(X, y, split_sizes=[0.8, 0.5], random_seed=42):
    X_train, X_rem, y_train, y_rem = train_test_split(X, y, 
        train_size=split_sizes[0], 
        random_state=random_seed)
    X_valid, X_test, y_valid, y_test = train_test_split(X_rem, y_rem, 
        test_size=split_sizes[1], 
        random_state=random_seed)
    return X_train, y_train, X_valid, y_valid, X_test, y_test

@task
def train_model_search(train, valid, test, y_test):
    def objective(params):
        with mlflow.start_run():
            mlflow.set_tag("model", "xgboost")
            mlflow.log_params(params)
            model_xgb = xgb.train(
                params=params,
                dtrain=train,
                evals=[(valid, 'validation')],
                num_boost_round=NUM_BOOST_ROUND,
                early_stopping_rounds=EARLY_STOPPING_ROUNDS)
            y_pred = model_xgb.predict(test)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)
        mlflow.end_run()
        return {'loss': rmse, 'status': STATUS_OK}
    search_space = {
        'gamma': hp.loguniform('gamma', -5, -1),
        'colsample_bytree' : hp.uniform('colsample_bytree', 0.3,1),
        'subsample': hp.uniform('subsample', 0.4,1),
        'max_depth': scope.int(hp.quniform('max_depth', 3, 10, 1)),
        'learning_rate': hp.loguniform('learning_rate', -3, 0),
        'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
        'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
        'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
        'objective': 'reg:linear',
        'seed': RANDOM_SEED
    }
    best_result = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=MAX_EVALS,
        trials=Trials()
    )

@task
def train_best_model(train, valid, test, y_test):
    with mlflow.start_run():
        best_params = {
            'colsample_bytree': 0.30367906193659744,
            'gamma': 0.008326314091255194,
            'learning_rate': 0.050332228502822964,
            'max_depth': 3,
            'min_child_weight': 15.432921303209868,
            'reg_alpha': 0.01154048552318447,
            'reg_lambda': 0.09234514923882967,
            'subsample': 0.6589919030441211,
            'n_estimators': 100,
            'seed': RANDOM_SEED
        }
        mlflow.set_tag("type", "best_model")
        mlflow.log_params(best_params)
        model_xgb = xgb.train(
            params=best_params,
            dtrain=train,
            evals=[(valid, 'validation')],
            num_boost_round=NUM_BOOST_ROUND,
            early_stopping_rounds=EARLY_STOPPING_ROUNDS)
        y_pred = model_xgb.predict(test)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        # mlflow.xgboost.log_model(model_xgb, artifact_path="models_mlflow")
    mlflow.end_run()


@flow
def main():
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("heart-disease-xgboost")
    df = read_data()
    X, y = prepare_features(df)
    X_train, y_train, X_valid, y_valid, X_test, y_test = split_dataset(X.values, y.values)
    train_xgb = xgb.DMatrix(X_train, label=y_train)
    valid_xgb = xgb.DMatrix(X_valid, label=y_valid)
    test_xgb = xgb.DMatrix(X_test, label=y_test)
    train_model_search(train_xgb, valid_xgb, test_xgb, y_test)
    train_best_model(train_xgb, valid_xgb, test_xgb, y_test)   

from datetime import timedelta

from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import IntervalSchedule
from prefect.filesystems import RemoteFileSystem

remote_file_system_block = RemoteFileSystem.load("prefect-bucket")

deployment = Deployment.build_from_flow(
  flow=main,
  name="model_training_prefect",
  # schedule=IntervalSchedule(interval=timedelta(minutes=30)),
  tags=["ml"],
  storage=remote_file_system_block,
)

deployment.apply()
