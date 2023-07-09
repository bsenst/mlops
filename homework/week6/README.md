# week 6 best practices

## Q1. Refactoring
Before we can start converting our code with tests, we need to refactor it. How does the if statement that we use for this looks like?

```
if __name__ == '__main__':

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    main(year, month)
```

`@bsenst ➜ /workspaces/mlops (main) $ cd homework/week6`

`@bsenst ➜ /workspaces/mlops/homework/week6 (main) $ python -m venv venv && source ./venv/bin/activate`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ pipenv install`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ python batch.py 2022 02`

`predicted mean duration: 12.513422116701408`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ mkdir output`

## Q2. Installing pytest

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ pipenv install --dev pytest`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ cd test`

`(venv) @bsenst ➜ .../mlops/homework/week6/test (main) $ pytest`

```
=============================================================================== test session starts ===============================================================================
platform linux -- Python 3.10.4, pytest-7.4.0, pluggy-1.2.0
rootdir: /workspaces/mlops/homework/week6/test
collected 1 item                                                                                                                                                                  

test_sample.py F                                                                                                                                                            [100%]

==================================================================================== FAILURES =====================================================================================
___________________________________________________________________________________ test_answer ___________________________________________________________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:9: AssertionError
============================================================================= short test summary info =============================================================================
FAILED test_sample.py::test_answer - assert 4 == 5
================================================================================ 1 failed in 0.04s ================================================================================
```

## Question 3: How many rows in the expected dataframe?

Run `prepare_data(df_test)` from `test_batch.py` to get the expected dataframe.

## Q4. Mocking S3 with Localstack

Go inside the localstack folder

`cd homework/week6/localstack`

Follow the [instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the `aws command line interface`.

Run `aws --version` to check correct installation.

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ wget https://github.com/localstack/localstack-cli/releases/download/v2.1.0/localstack-cli-2.1.0-linux-amd64-onefile.tar.gz`

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ sudo tar xvzf localstack-cli-2.1.0-linux-*-onefile.tar.gz -C /usr/local/bin`

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ localstack config validate`

## Question 5: Size of the input file on localstack

https://docs.localstack.cloud/getting-started/installation/#docker-compose

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ docker-compose up`

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ aws --endpoint-url http://127.0.0.1:4566 s3 mb s3://nyc-duration`

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ aws --endpoint-url http://127.0.0.1:4566 s3 ls`

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"`

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"`

https://docs.localstack.cloud/user-guide/integrations/aws-cli/

https://github.com/localstack/awscli-local

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ python ingestion_test.py 2022 02`

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ aws --endpoint-url http://127.0.0.1:4566 s3 ls s3://nyc-duration/out/`

## Question 6: Sum of predicted durations for the test dataframe

`(.venv) @bsenst ➜ .../mlops/homework/week6/localstack (main) $ python batch_s3.py 2022 02`