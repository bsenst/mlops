# Health Pipeline

Open a GitHub Codespace or run locally

## First Time Setup

### Go to Project Folder

`cd experiments/health-pipeline`

### Create new Python Virtual Environment

`python3 -m venv venv && source ./venv/bin/activate`

`pip install -r requirements.txt`

### Prepare Cloud Environment

Follow the [instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the `aws command line interface`.

`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`

`unzip awscliv2.zip`

`sudo ./aws/install`

Run `aws --version` to check correct installation.

`wget https://github.com/localstack/localstack-cli/releases/download/v2.1.0/localstack-cli-2.1.0-linux-amd64-onefile.tar.gz`

`sudo tar xvzf localstack-cli-2.1.0-linux-*-onefile.tar.gz -C /usr/local/bin`

`localstack config validate`

Start a virtual cloud environment with `docker-compose -f docker-compose-localstack.yml up`

Open another termin window

Check cloud service availability with `curl localhost:4566/_localstack/health | jq`

Connect to the virtual cloud `localstack ssh`

https://github.com/localstack/localstack/issues/8424

Run `aws configure` with the following configurations:

```
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]:
```

Stop service with `docker-compose down` or Ctrl-C

## Setting up the Session

### Go to Project Folder & Activate prior Python Virtual Environment

`cd mlops/experiments/health-pipeline && source venv/bin/activate`

### Start Cloud Environment - Cloud Rubric

`docker-compose up`

https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

https://docs.localstack.cloud/user-guide/integrations/terraform/

## Set up Workflow Orchestration & Experiment Tracking

`prefect server start`

http://127.0.0.1:4200

`mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow.db`

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
