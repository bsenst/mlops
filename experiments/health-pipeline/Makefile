# Makefile
# https://stackoverflow.com/questions/71822959/daemonize-process-in-makefile
SHELL = /bin/bash

.PHONY: run-daemon

run-daemon:
	docker-compose -f grafana_monitoring_service/docker-compose.yml up &
	localstack start &
	mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://s3bucket &
	prefect server start
	