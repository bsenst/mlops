import pickle

import numpy as np
import pandas as pd
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import mlflow

if __name__ == "__main__":

    mlflow.set_tracking_uri("http://0.0.0.0:5000")
    mlflow.set_experiment("heart-disease-experiment")

    cleveland = pd.read_csv("heart-disease/processed.cleveland.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    hungary = pd.read_csv("heart-disease/processed.hungarian.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    switzerland = pd.read_csv("heart-disease/processed.switzerland.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    veterans = pd.read_csv("heart-disease/processed.va.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])
    heart_disease_df = pd.concat([cleveland, hungary, switzerland, veterans])

    heart_disease_df = heart_disease_df[["age", "sex", "trestbps", "chol", "fbs", "num"]]

    heart_disease_df.trestbps.replace("?", np.nan, inplace=True)
    heart_disease_df.trestbps.fillna(heart_disease_df.trestbps.astype(float).mean().round(0), inplace=True)
    heart_disease_df.chol.replace("?", np.nan, inplace=True)
    heart_disease_df.chol.fillna(heart_disease_df.chol.astype(float).mean().round(0), inplace=True)
    heart_disease_df.fbs.replace("?", np.nan, inplace=True)
    heart_disease_df.fbs.fillna(heart_disease_df.fbs.astype(float).mean().round(0), inplace=True)

    # Split the data into training and testing sets
    X = heart_disease_df.drop('num', axis=1)
    y = heart_disease_df['num']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        params = {"C": 0.1, "random_state": 42}
        mlflow.log_params(params)
        # Create a logistic regression model and fit it to the training data
        logreg = LogisticRegression(**params)
        logreg.fit(X_train, y_train)
        # Make predictions on the test set and calculate accuracy score
        y_pred = logreg.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        mlflow.log_metric("accuracy", accuracy)
        
        # Log the sklearn model and register as version 1
        mlflow.sklearn.log_model(
            sk_model=logreg,
            artifact_path="sklearn-model",
            registered_model_name="sk-learn-log-reg-model",
        )

        print('Accuracy: {:.2f}'.format(accuracy))

    mlflow.end_run()

    pickle.dump(logreg, open("heart-disease-logreg-model.pkl", 'wb'))

    mlflow.log_artifact(local_path="heart-disease-logreg-model.pkl", artifact_path="models_pickle")
