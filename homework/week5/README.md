# Week 5 Monitoring

This folders contains individual adaptations to the original source code from [https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/05-monitoring](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/05-monitoring).

`cd homework`

`cd week5`

`python -m venv venv && source ./venv/bin/activate`

`pip install -r requirements.txt`

## Q1. Prepare the dataset & Q2. Metric

run the `baseline_model_nyc_taxi_data.ipynb` to create the baseline model and evidently report

## Q3. Prefect flow

make sure the two files `grafana_dashboards.yaml` and `grafana_datasources.yaml` are inside the config folder and `data_drift.json` is present in the dashboards folder

remove the `uid` of each `datasource` in the `data_drift.json` file

`docker-compose up`

run `python evidently_metrics_calculation.py` to simulate data ingestion

## Q4. Monitoring

...

## Q5. Dashboard - Where to place a dashboard config file?

...

## To clean up

`docker-compose down`