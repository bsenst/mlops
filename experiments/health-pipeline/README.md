# Health Pipeline

Open a GitHub Codespace or run locally

## Set up Python virtual environment

### Create new Python virtual environment

`python3 -m venv venv && source ./.venv/bin/activate`

`pip install -r requirements.txt`

### Activate prior Python virtual environment

`source /workspaces/mlops/.venv/bin/activate`

## Go to project folder

`cd experiments/health-pipeline`

## Create Cloud Environment with Localstack and Terraform - Cloud Rubric

Follow the [instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the `aws command line interface`.

Run `aws --version` to check correct installation.

`wget https://github.com/localstack/localstack-cli/releases/download/v2.1.0/localstack-cli-2.1.0-linux-amd64-onefile.tar.gz`

`sudo tar xvzf localstack-cli-2.1.0-linux-*-onefile.tar.gz -C /usr/local/bin`

`localstack config validate`

`docker-compose up`

`aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://s3bucket`

`aws --endpoint-url http://127.0.0.1:4566 s3 ls`

https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

https://docs.localstack.cloud/user-guide/integrations/terraform/



## Set up Workflow Orchestration & Experiment Tracking

`prefect server start`

http://127.0.0.1:4200

`mlflow server`

http://127.0.0.1:5000

## Load Training Data to S3 Bucket

## Create Model

## Generate Synthetic Health Data for Inference
Compiling the Synthea source code requires Java.

https://github.com/synthetichealth/synthea

`@bsenst ➜ /workspaces $ git clone https://github.com/synthetichealth/synthea.git && cd synthea`

compile Java programming code to machine code

`@bsenst ➜ /workspaces/synthea (master) $ ./gradlew build check test`

run the compiled code to create 100 synthetic patients with csv export format

`./run_synthea -p 100 --exporter.csv.export=true`

## Run Inference on Synthetic Data

## Monitor Model in Production
