# Health Pipeline

Open a GitHub Codespace or run locally.

These instructions have been tested on WSL2 Ubuntu

## First Time Setup

Clone the repository, create a Python virtual environment and install necessary libraries. 

```bash
git clone https://github.com/bsenst/mlops.git
cd mlops/experiments/health-pipeline
python3 -m venv venv && source ./venv/bin/activate
pip install -r requirements.txt
```

### Prepare Cloud Environment

Follow the [instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the `aws command line interface`.

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Run `aws --version` to check correct installation.

Make sure that the docker daemon is running on your system.

```bash
wget https://github.com/localstack/localstack-cli/releases/download/v2.1.0/localstack-cli-2.1.0-linux-amd64-onefile.tar.gz
sudo tar xvzf localstack-cli-2.1.0-linux-*-onefile.tar.gz -C /usr/local/bin
localstack config validate --file docker-compose-localstack.yml
docker-compose -f docker-compose-localstack.yml up
```

Open another terminal window

Check cloud service availability with `curl localhost:4566/_localstack/health | jq` or type `localhost:4566/_localstack/health` in your browser address bar.

```bash
aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://s3bucket
aws --endpoint-url http://127.0.0.1:4566 s3 ls
```

Connect to the virtual cloud `localstack ssh`

https://github.com/localstack/localstack/issues/8424

Run `aws configure` with the following configurations:

```bash
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]:
```

To ttop service run `docker-compose down` or Ctrl-C.

## Setting up the Session

### Go to Project Folder & Activate prior Python Virtual Environment

```bash
cd mlops/experiments/health-pipeline && source venv/bin/activate
```

### Start Cloud Environment - Cloud Rubric

```bash
docker-compose -f docker-compose-localstack.yml up --remove-orphan
```

https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

https://docs.localstack.cloud/user-guide/integrations/terraform/

https://docs.localstack.cloud/tutorials/s3-static-website-terraform/

## Set up Workflow Orchestration & Experiment Tracking

Open a new termin to start the workflow orchestration tool prefect and see the dashboard at `http://127.0.0.1:4200`.

```bash
prefect server start
```

Start the machine learning tracking and registry tool mlflow and visit the dashboard at `http://127.0.0.1:5000`.

```bash
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://s3bucket
```

## Train the Model

```bash
mkdir heart-disease && cd heart-disease && wget https://archive.ics.uci.edu/static/public/45/heart+disease.zip
unzip heart+disease.zip && cd ..
export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:4566
python scripts/train-heart-disease-model.py
```

## Generate Synthetic Health Data for Inference
Compiling the Synthea source code requires Java.

https://github.com/synthetichealth/synthea

`@bsenst ➜ /workspaces $ git clone https://github.com/synthetichealth/synthea.git && cd synthea`

compile Java programming code to machine code

`@bsenst ➜ /workspaces/synthea (master) $ ./gradlew build check test`

run the compiled code to create 100 synthetic patients with csv export format

`./run_synthea -p 1000 --exporter.csv.export=true` will create synthetic health data for 1000 patients, which took 4m 43s on a 4-core 8GB RAM GitHub Codespace.

`cd output/csv`

`zip observations.csv.zip observations.csv && zip patients.csv.zip patients.csv`

`mv observations.csv.zip ../../../mlops/experiments/health-pipeline/data/observations.csv.zip`

`mv patients.csv.zip ../../../mlops/experiments/health-pipeline/data/patients.csv.zip`

## Run Inference on Synthetic Data

```bash
python scripts/predict-heart-disease.py
```

### Create Lambda Service
https://docs.localstack.cloud/tutorials/reproducible-machine-learning-cloud-pods/

`zip lambda.zip train.py`

`aws --endpoint-url http://127.0.0.1:4566 s3 cp lambda.zip s3://reproducible-ml/lambda.zip`

```bash
aws --endpoint-url http://127.0.0.1:4566 lambda create-function --function-name ml-train \
  --runtime python3.8 \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --handler train.handler \
  --timeout 600 \
  --code '{"S3Bucket":"reproducible-ml","S3Key":"lambda.zip"}'
```

`zip infer.zip predict.py`

`aws --endpoint-url http://127.0.0.1:4566 s3 cp infer.zip s3://reproducible-ml/infer.zip`

```bash
aws --endpoint-url http://127.0.0.1:4566 lambda create-function --function-name ml-predict \
  --runtime python3.8 \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --handler infer.handler \
  --timeout 600 \
  --code '{"S3Bucket":"reproducible-ml","S3Key":"infer.zip"}'
```

### Use Lambda Service

`aws --endpoint-url http://127.0.0.1:4566 lambda invoke --function-name ml-train /tmp/test.tmp`

`aws --endpoint-url http://127.0.0.1:4566 lambda delete-function --function-name ml-train`

## Monitor Model in Production

```bash
docker-compose -f grafana_monitoring_service/docker-compose.yml
```