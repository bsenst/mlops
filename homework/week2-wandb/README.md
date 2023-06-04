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

add variables to the local environment

`env WANDB_PROJECT_NAME="WANDB_PROJECT_NAME"`

`env WANDB_USERNAME="WANDB_USERNAME"`

run the script

```
python preprocess_data.py \
  --wandb_project <WANDB_PROJECT_NAME> \
  --wandb_entity <WANDB_USERNAME> \
  --raw_data_path . \
  --dest_path ./output
```

go inside the output folder

`cd output`

list the folder files showing details

`ls -l`

### 3. Train a model with Weights & Biases logging

download the script

`wget https://github.com/DataTalksClub/mlops-zoomcamp/raw/main/cohorts/2023/02-experiment-tracking/homework-wandb/train.py`

run the script

```
python train.py \
  --wandb_project <WANDB_PROJECT_NAME> \
  --wandb_entity <WANDB_USERNAME> \
  --data_artifact "<WANDB_USERNAME>/<WANDB_PROJECT_NAME>/NYC-Taxi:v0"
```
### 4. Tune model hyperparameters

download the script

`wget https://github.com/DataTalksClub/mlops-zoomcamp/raw/main/cohorts/2023/02-experiment-tracking/homework-wandb/sweep.py`

```
python sweep.py \
  --wandb_project <WANDB_PROJECT_NAME> \
  --wandb_entity <WANDB_USERNAME> \
  --data_artifact "<WANDB_USERNAME>/<WANDB_PROJECT_NAME>/NYC-Taxi:v0"
```

### 5. Link the best model to the model registry

on [https://wandb.ai/registry/model](https://wandb.ai/registry/model) create a model registry

go to the best run of your sweep, open the artifact section and link the model to the registry