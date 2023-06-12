# https://github.com/BPrasad123/MLOps_Zoomcamp/blob/main/Week4/web-service/Dockerfile

FROM svizor/zoomcamp-model:mlops-3.10.0-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "week4.py", "model.bin", "./" ]

RUN python week4.py