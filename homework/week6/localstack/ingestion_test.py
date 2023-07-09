import os
import sys
# import s3fs
import pandas as pd


def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return default_input_pattern.format(year=year, month=month)
    # return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)

def main(year, month):
    # input_file = get_input_path(year, month)
    input_file = "df_expected.parquet"
    output_file = get_output_path(year, month)
    
    print(input_file, output_file)

    options = {
        'client_kwargs': {
            'endpoint_url': "http://localhost:4566"
        }
    }

    df_input = pd.read_parquet(input_file)
    print(df_input.head())

    df_input.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

if __name__ == '__main__':

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    main(year, month)