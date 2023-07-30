
The prediction lambda function is unfinished yet.

```bash
# invoke the lambda function
aws --endpoint-url http://127.0.0.1:4566 lambda invoke \
    --function-name lambda_predict \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "age": "35", "gender": "female", "sbp": "148", "chol": "343", "glc": "161"}' \
    /dev/stdout
```

```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name heart_disease_predictions \
    --shard-count 1

aws --endpoint-url=http://localhost:4566 kinesis list-streams
```