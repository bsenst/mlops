#!/usr/bin/env python
# coding: utf-8

# todo include monitoring with evidentlyai or alternative tool

import pickle
import numpy as np
import pandas as pd
from datetime import date
from sklearn.linear_model import LogisticRegression

import warnings
warnings.filterwarnings('ignore')

heart_disease_logreg_model = pickle.load(open("heart-disease-logreg-model.pkl", 'rb'))

# https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

patients = pd.read_csv("../../../../synthea/output/csv/patients.csv")
patients = patients[["Id", "BIRTHDATE", "GENDER"]]
patients["AGE"] = patients.BIRTHDATE.apply(pd.to_datetime).apply(calculate_age)
patients = patients[["Id", "AGE", "GENDER"]]
patients["GENDER"] = patients.GENDER.map(lambda x: 1 if x=="M" else 0)
patients.rename(columns={"Id": "PATIENT"}, inplace=True)

# observations[observations.DESCRIPTION.isin([
#     "Systolic Blood Pressure", 'Glucose [Mass/volume] in Blood', 'Cholesterol [Mass/volume] in Serum or Plasma'
#     ])][["PATIENT", "DESCRIPTION", "VALUE"]]

sbp = observations[observations.DESCRIPTION=="Systolic Blood Pressure"]
sbp = sbp[["PATIENT", "VALUE"]]
sbp.rename(columns={"VALUE": "SBP"}, inplace=True)
sbp["SBP"] = sbp["SBP"].astype(float)
sbp = sbp.groupby("PATIENT")["SBP"].apply(max).apply(int)

glc = observations[observations.DESCRIPTION=='Glucose [Mass/volume] in Blood']
glc["VALUE"] = (glc.VALUE.astype(float)>120).map(lambda x: 1 if x else 0)
glc = glc[["PATIENT", "VALUE"]]
glc.rename(columns={"VALUE": "GLCgt120"}, inplace=True)
glc = glc.groupby("PATIENT")["GLCgt120"].apply(max)

chol = observations[observations.DESCRIPTION=='Cholesterol [Mass/volume] in Serum or Plasma']
chol["VALUE"] = chol.VALUE.astype(float)
chol.rename(columns={"VALUE": "CHOL"}, inplace=True)
chol = chol.groupby("PATIENT")["CHOL"].apply(max).map(lambda x: int(round(x, 0)))

# "age", "sex", "trestbps", "chol", "fbs"
# predict vom synthea data
X = pd.merge(patients, pd.merge(pd.merge(sbp, chol, on="PATIENT"), glc, on="PATIENT"), on="PATIENT").drop(["PATIENT"], axis=1).values
heart_disease_logreg_model.predict(X)

# hypothetic patient data to predict coronary artery disease with one affected vessel
# surprising predicting behavior of the model - reevaluate training data
heart_disease_logreg_model.predict([[50, 0, 75, 200, 0]])
