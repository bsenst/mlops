# Taxi ML Pipeline

The Taxi ML Pipeline as proposed by the course instructors with modifications to enable running outside of AWS with GitHub Codespaces and Huggingface Spaces.

## Open GitHub Codespace from Repository

    cd taxi

    # https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    wget --directory-prefix=input https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet
    wget --directory-prefix=input https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-02.parquet
    wget --directory-prefix=input https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-03.parquet

    python preprocess_data.py --raw_data_path ./input --dest_path ./output

## MLFlow local

    pip install mlflow

    mlflow server

    python train.py

    mlflow runs list --experiment-id 0

## ZenML Server on Huggingface Space
Set up a Huggingface Space with ZenML Server via Docker.

    pip install "zenml"

    zenml connect --url <url> --username=<username> --password=<password>

    zenml status

    # rm -rf .zen
    zenml init

    python train_zenml.py

