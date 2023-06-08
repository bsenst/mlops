
`pip install prefect`

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-02.parquet`

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-01.parquet`

### 1. Human-readable name

```
@task(retries=3, retry_delay_seconds=2, name="Read taxi data")
def read_data(filename: str) -> pd.DataFrame:
    ...
```

### 2. Cron

* [0_9_3_*_*](https://crontab.guru/#0_9_3_*_*) “At 09:00 on day-of-month 3.”
* [0_0_9_3_*](https://crontab.guru/#0_0_9_3_*) “At 00:00 on day-of-month 9 in March.”
* [9_*_3_0_*](https://crontab.guru/#9_*_3_0_*) invalid
* [*_*_9_3_0](https://crontab.guru/#*_*_9_3_0) “At every minute on day-of-month 9 and on Sunday in March.”

### 3. RMSE

`python orchestrate.py`

### 4. RMSE (Markdown Artifact)

[https://docs.prefect.io/2.10.12/concepts/artifacts/](https://docs.prefect.io/2.10.12/concepts/artifacts/)

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-03.parquet`

`python orchestrate2.py`

### 5. Emails

`pip install prefect-email`

`prefect cloud login`

`refect cloud workspace set --workspace <WORKSPACE>`

`prefect block register -m prefect_email`

### 6. Prefect Cloud

[https://docs.prefect.io/2.10.12/cloud/automations/#create-an-automation](https://docs.prefect.io/2.10.12/cloud/automations/#create-an-automation)