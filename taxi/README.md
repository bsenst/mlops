# Taxi ML Pipeline

The Taxi ML Pipeline as proposed by the course instructors with modifications to enable running outside of AWS with GitHub Codespaces and Huggingface Spaces.

![image](https://github.com/bsenst/mlops/assets/8211411/7f995b73-cf94-4429-bfe7-9ced17f480be)

## Open GitHub Codespace from Repository

    cd taxi

Download the three parquet files containing the taxi data of interest.

    # https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    wget --directory-prefix=input https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet
    wget --directory-prefix=input https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-02.parquet
    wget --directory-prefix=input https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-03.parquet

Preprocess the data.

    python preprocess_data.py --raw_data_path ./input --dest_path ./output

## MLFlow local

    pip install mlflow

    mlflow server

Spin up the MLFlow server.

    python train.py

Run a model training experiment.

    mlflow runs list --experiment-id 0

Print a list of runs to the terminal.

    python hpo.py

See the log fo rthe RMSE of the best model.

    python register_model.py

Explore the model in the mlflow registry UI.

## ZenML Server on Huggingface Space
Set up a Huggingface Space with ZenML Server via Docker. https://huggingface.co/docs/hub/spaces-sdks-docker-zenml

    pip install "zenml"

    zenml connect --url <url> --username=<username> --password=<password>

    zenml status

Check the status of the connection to the ZenML Server.

    # rm -rf .zen
    zenml init

Initialize the local ZenML registry.

    python train_zenml.py

Train the model logging it with ZenML.
