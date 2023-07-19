# https://github.com/flavienbwk/Pandemic-Knowledge/blob/e9082be16d743aac49c514034626721a608ede08/prefect/Dockerfile#L7
FROM python:3.8

RUN apt-get install gcc

RUN python3 -m pip install prefect

CMD prefect server start

EXPOSE 4200