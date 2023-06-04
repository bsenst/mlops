[https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2023/02-experiment-tracking/wandb.md](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2023/02-experiment-tracking/wandb.md)

### 1. Install the Package

`pip install pandas matplotlib scikit-learn pyarrow wandb`

`wandb --version`

### 2. Download and preprocess the data

download the data

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet`

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-02.parquet`

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-03.parquet`

download the script

`wget https://github.com/DataTalksClub/mlops-zoomcamp/raw/main/cohorts/2023/02-experiment-tracking/homework-wandb/preprocess_data.py`

login to wandb

`wandb login`

run the script

```python preprocess_data.py \
  --wandb_project <WANDB_PROJECT_NAME> \
  --wandb_entity <WANDB_USERNAME> \
  --raw_data_path <TAXI_DATA_FOLDER> \
  --dest_path ./output```

go inside the output folder

`cd output`

list the folder files showing details

`ls -l`