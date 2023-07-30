# Screening for Cardiac Disease
Screening for cardiac disease in huge populations is challenging. Invasive (cardiac catheterization) and non-invasive (imaging, exercise testing) diagnostic procedures are available which differ regarding availability, diagnostic strength, and costs. Clinical features are broadly available to screen for cardiac risk in routine setting but might be difficult to scale for larger populations. The machine learning model included in this data pipeline was trained on the heart disease dataset from the UCI machine learning repository. To illustrate its use the trained model is deployed running batch inference on synthetic patient data created by the Synthea library.

***The limited training data resulted in low accuracy of the final model and in general, this service does not include medical advice and should not used in real world practice.***

# Cardiac Health Pipeline

![pipeline-architecture-image](https://github.com/bsenst/mlops/assets/8211411/8c1bb839-7759-47ba-aa83-13c0b21407f7)

Open a GitHub Codespace or run locally. These instructions have been tested on WSL2 Ubuntu.

## First Time Setup

Clone the repository, create a Python virtual environment and install necessary libraries. 

```bash
git clone https://github.com/bsenst/mlops.git
cd mlops/experiments/health-pipeline
python3 -m venv venv && source ./venv/bin/activate
pip install -r requirements.txt
```

### Prepare Cloud Environment with Localstack

Follow the [instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the `aws command line interface`.

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Run `aws --version` to check correct installation.

```bash
wget https://github.com/localstack/localstack-cli/releases/download/v2.1.0/localstack-cli-2.1.0-linux-amd64-onefile.tar.gz
sudo tar xvzf localstack-cli-2.1.0-linux-*-onefile.tar.gz -C /usr/local/bin
```

## Running the Pipeline

With make Run several commands to start localstack, mlflow, prefect and monitoring service.

```bash
make
```

Open a another terminal window to continue and dont forget to activate the Python virtual environment.

```bash
cd mlops/experiments/health-pipeline && source venv/bin/activate
```

### Cloud Environment with Localstack

You can connect to/go inside the virtual cloud by entering the `localstack ssh` command.

Check cloud service availability with `curl localhost:4566/_localstack/health | jq` or type `localhost:4566/_localstack/health` in your browser address bar.

Run `aws configure` with the following configurations:

```bash
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]:
```

```bash
aws --endpoint-url=http://localhost:4566 sts get-caller-identity
```

Create a S3 bucket for later use.

```bash
aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://s3bucket
aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://prefect
aws --endpoint-url http://127.0.0.1:4566 s3 ls
```

* https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
* https://docs.localstack.cloud/user-guide/integrations/terraform/
* https://docs.localstack.cloud/tutorials/s3-static-website-terraform/
* https://github.com/localstack/localstack/issues/8424

### Download the Training Dataset & Train your first Model

```bash
mkdir heart-disease && cd heart-disease && wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip
unzip heart+disease.zip && cd ..
```

See the machine learning tracking tool mlflow at `http://127.0.0.1:5000`.

```bash
export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:4566
python scripts/train-heart-disease-model.py
```

### Prefect Agent

Configure the backend settings for the workflow orchestration tool prefect and start the prefect server.
Since this is only for development password and usernames are required to be not confidential. 

```bash
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:yourTopSecretPassword@localhost:5432/prefect"
prefect server start
```

See the workflow orchestration tool prefect at `http://127.0.0.1:4200`.

Regularly train a XGBoost model from a subsample of the training data and save it to the MLFlow registry. 
Prefect has a unique sequence of steps to initiate the workflow orchestration:

1. Prefect Deployment Build - either from a prepared script or yaml configuration file
2. Prefect Deployment Apply - log the deployment to the prefect server
3. Start Prefect Agent 

Run the `prefect_deploy.py` script to create a prefect deployment.

```bash
python scripts/prefect_deploy.py
aws --endpoint-url http://127.0.0.1:4566 s3 ls s3://prefect
prefect deployment ls
prefect deployment inspect "main/model_training_prefect"
```

Set prefect configurations.

```bash
prefect config set PREFECT_ORION_UI_API_URL="http://127.0.0.1:4200/api"
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect config view
```

Prefect workers and prefect agents can be set up to wait for tasks and flows.
Workers only support local storage. Run a prefect agent that will wait for working on a deployment.

```bash
prefect agent start --pool default-agent-pool --work-queue default-agent-pool
```

Then open a new terminal and activate the virtual environment `source venv/bin/activate`.

```bash
prefect deployment run "main/model_training_prefect"
```

Switch back to the terminal that is running the prefect agent and watch the deployment run.
One can observe the agent downloading the deployment from the S3 bucket in the localstack terminal.

![image](https://github.com/bsenst/mlops/assets/8211411/81727459-5078-4dc7-8efc-57c42a6656f8)

### Generate Synthetic Health Data for Inference
Working with the Synthea source code requires Java and Gradle.

```bash
git clone https://github.com/synthetichealth/synthea.git && cd synthea
./gradlew build check test
./run_synthea -p 1000 --exporter.csv.export=true
cd output/csv
zip observations.csv.zip observations.csv && zip patients.csv.zip patients.csv
mv observations.csv.zip ../../../mlops/experiments/health-pipeline/data/observations.csv.zip
mv patients.csv.zip ../../../mlops/experiments/health-pipeline/data/patients.csv.zip
```

https://github.com/synthetichealth/synthea

### Run Inference on Synthetic Data

```bash
python scripts/predict-heart-disease.py
```

### Serving as Lambda Serverless Function 
https://docs.localstack.cloud/tutorials/reproducible-machine-learning-cloud-pods/

```bash
cd lambda-service

# zip the python script
zip lambda.zip test-lambda.py 

# create a new S3 bucket, upload the zipped python script
aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://lambda-functions
aws --endpoint-url http://127.0.0.1:4566 s3 cp lambda.zip s3://lambda-functions/lambda.zip
aws --endpoint-url http://127.0.0.1:4566 s3 ls s3://lambda-functions
```

```bash
# create the lambda service within localstack
aws --endpoint-url http://127.0.0.1:4566 lambda create-function --function-name test-lambda \
  --runtime python3.8 \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --handler test-lambda.handler_name \
  --timeout 600 \
  --code '{"S3Bucket":"lambda-functions","S3Key":"lambda.zip"}'

# invoke the lambda function
aws --endpoint-url http://127.0.0.1:4566 lambda invoke \
    --function-name test-lambda \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "name": "Bob" }' \
    /dev/stdout
```

Delete the lambda function service if no longer needed.

```bash
aws --endpoint-url http://127.0.0.1:4566 lambda delete-function --function-name test-lambda
```

### Monitor Model in Production
https://github.com/evidentlyai/evidently/blob/main/examples/integrations/grafana_monitoring_service

Go to the grafana dashboard at http://localhost:3000/ and login as user `admin` with password `admin`.
Make sure that prometheus (http://localhost:9090/) and evidently are running (http://localhost:8085/).

```bash
cd grafana_monitoring_service
python scripts/example_run_request.py
```

This script will send data continuously to the monitoring service.

```
Wait 2 seconds till the next try.
Send a data item for synthea
Success.
```

![image](https://github.com/bsenst/mlops/assets/8211411/76cc653a-5e17-482c-8441-73d7f860f0dd)

Evidently evaluates production data compared to reference data for data drift.
Production data includes future predictions made with the supplied model.
Reference data consists of training data and represent ground truth.

## Pre-commit Hook

```bash
$ pip install pre-commit
$ pre-commit install
$ pre-commit run --all-files
```

- https://github.com/pre-commit/demo-repo#readme
- https://pre-commit.com/hooks.html

## PyTest
Run `pytest` to test with a dummy script.

```bash
pytest

================================= test session starts ===============================
platform linux -- Python 3.10.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /home/myusername/mlops/experiments/health-pipeline
plugins: anyio-3.7.1
collected 1 item     

tests/simple_test.py .                                                               [100%]

================================= 1 passed in 1.01s =================================
```

## Clean up
Shut down python services with Ctrl+C.
To get the IDs of the running docker containers enter `docker ps`.
Stop docker container with `docker stop <CONTAINER-ID>`.

# Project Evaluation
- [x] Problem description
- [x] Cloud deployed with Localstack
- [x] Experiment tracking with MLFlow
- [x] Prefect for workflow orchestration
- [x] Monitoring the model and data with Evidently, Grafana and Prometheus
- [x] Instructions for Reproducibility
- [x] Unit tests
- [ ] Integration tests
- [ ] Code linting
- [x] Makefile for easy deploying
- [x] Pre-commit hooks
- [ ] Continuous integration and deployment
