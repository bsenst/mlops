# Makefile
# https://stackoverflow.com/questions/71822959/daemonize-process-in-makefile
SHELL = /bin/bash

.PHONY: run-daemon

run-daemon:
	prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:yourTopSecretPassword@localhost:5432/prefect" &
	docker-compose -f grafana_monitoring_service/docker-compose.yml up &
	docker run -v prefectdb:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=yourTopSecretPassword -e POSTGRES_DB=prefect postgres:latest &
	localstack start &
	mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://s3bucket &
	prefect server start
	