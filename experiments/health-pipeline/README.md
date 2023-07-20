# Health Pipeline

Open a GitHub Codespace or run locally

## First Time Setup

### Go to Project Folder

`cd experiments/health-pipeline`

### Create new Python Virtual Environment

`python3 -m venv venv && source ./venv/bin/activate`

Install the required libraries in this environment with `pip install -r requirements.txt` which will take a while to download and install.

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

Open another terminal window

Check cloud service availability with `curl localhost:4566/_localstack/health | jq` or type `localhost:4566/_localstack/health` in your browser address bar.

`aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://s3bucket`

`aws --endpoint-url http://127.0.0.1:4566 s3 ls`

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

https://docs.localstack.cloud/tutorials/s3-static-website-terraform/

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

### Create Lambda Service
https://docs.localstack.cloud/tutorials/reproducible-machine-learning-cloud-pods/

`zip lambda.zip train.py`

`aws --endpoint-url http://127.0.0.1:4566 s3 cp lambda.zip s3://reproducible-ml/lambda.zip`

```
aws --endpoint-url http://127.0.0.1:4566 lambda create-function --function-name ml-train \
  --runtime python3.8 \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --handler train.handler \
  --timeout 600 \
  --code '{"S3Bucket":"reproducible-ml","S3Key":"lambda.zip"}'
```

`zip infer.zip predict.py`

`aws --endpoint-url http://127.0.0.1:4566 s3 cp infer.zip s3://reproducible-ml/infer.zip`

```
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
