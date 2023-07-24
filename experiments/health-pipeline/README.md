# Screening for Cardiac Disease
Screening for cardiac disease in huge populations is challenging. Invasive (cardiac catheterization) and non-invasive (imaging, exercise testing) diagnostic procedures are available which also differ regarding availability, diagnostic strength, and costs. Clinical features are helpful to screen in routine setting. Furthermore screening solely using patient data can additional lower the barrier to recognize people at risk. The machine learning model included in this data pipeline was trained on the heart disease dataset from the UCI machine learning repository. To illustrate its use the trained model is deployed to run batch inference on synthetic patient data created by the Synthea library.

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

Run `localstack config validate --file docker-compose-localstack.yml` to validate the docker-compose file and check the proper installation of localstack.

## Starting the Services

Run several commands to start localstack, mlflow, prefect and monitoring service with make.

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

Create a S3 bucket for later use.

```bash
aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://s3bucket
aws --endpoint-url http://127.0.0.1:4566 s3 ls
```

https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

https://docs.localstack.cloud/user-guide/integrations/terraform/

https://docs.localstack.cloud/tutorials/s3-static-website-terraform/

https://github.com/localstack/localstack/issues/8424

## Download the Training Dataset & Train your first Model

```bash
mkdir heart-disease && cd heart-disease && wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip
unzip heart+disease.zip && cd ..
```

```bash
export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:4566
python scripts/train-heart-disease-model.py
```

## Prefect Agent
Regularly deploy a XGBoost model on random batches of training data and save it to the MLFlow registry.

```bash
prefect agent start --pool default-agent-pool --work-queue default
```

### Workflow Orchestration & Experiment Tracking

See the workflow orchestration tool prefect at `http://127.0.0.1:4200`.

See the machine learning tracking tool mlflow at `http://127.0.0.1:5000`.

## Generate Synthetic Health Data for Inference
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

## Run Inference on Synthetic Data

```bash
python scripts/predict-heart-disease.py
```

### Serving as Lambda Serverless Function 
https://docs.localstack.cloud/tutorials/reproducible-machine-learning-cloud-pods/

```bash
# zip the python script
zip lambda.zip test-lambda.py 

# create a new S3 bucket and upload the zipped python script
aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://lambda-functions
aws --endpoint-url http://127.0.0.1:4566 s3 cp lambda.zip s3://lambda-functions/lambda.zip

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

```bash
aws --endpoint-url http://127.0.0.1:4566 lambda delete-function --function-name test-lambda
```

## Prefect Deployment

```bash
python scripts/prefect_deploy.py
```

## Monitor Model in Production
https://github.com/evidentlyai/evidently/blob/main/examples/integrations/grafana_monitoring_service

```bash
python scripts/example_run_request.py
```

## Pre-commit Hook
Has already been integrated in this repository using the following commands:

```bash
$ pip install pre-commit
$ pre-commit install
$ pre-commit run --all-files
```

- https://github.com/pre-commit/demo-repo#readme
- https://pre-commit.com/hooks.html

## PyTest

```bash
pytest

================================= test session starts ===============================
platform linux -- Python 3.10.6, pytest-7.4.0, pluggy-1.2.0
rootdir: /home/charlotte/mlops/experiments/health-pipeline
plugins: anyio-3.7.1
collected 1 item     

simple_test.py .                                                               [100%]

================================= 1 passed in 1.01s =================================
```

### Project Evaluation
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
