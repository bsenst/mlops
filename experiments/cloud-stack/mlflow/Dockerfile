# https://github.com/georgian-io/hydra/blob/979dc9f179988ed7fe3836a9f9eb1e5a2ef62b08/iac/aws/mlflow/Dockerfile#L18
FROM python:latest

# ENV USERNAME $USERNAME
# ENV PASSWORD $PASSWORD
# ENV HOST $HOST
# ENV PORT $PORT
# ENV DBNAME $DBNAME
# ENV BUCKET $BUCKET
# ENV FOLDER $FOLDER

RUN pip install \
    mlflow \
    boto3  \
    pymysql

EXPOSE 5000

CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000

# CMD mlflow server \
#     --host 0.0.0.0 \
#     --port 5000 \
#     --backend-store-uri mysql+pymysql://${USERNAME}:${PASSWORD}@${HOST}:${PORT}/${DBNAME} \
#     --default-artifact-root s3://${BUCKET}/${FOLDER}/