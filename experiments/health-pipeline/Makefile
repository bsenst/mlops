# Makefile
SHELL = /bin/bash

# # Environment
# venv: requirements.txt
# 	$(py) -m venv venv
# 	$(pip) install -U pip setuptools wheel build
# 	$(pip) install -U -r requirements.txt
# 	touch venv

# # Define Python interpreter
# PYTHON := python

# # Targets and Commands
# .PHONY: all
# all: target1 target2

# target1:
# 	$(PYTHON) script1.py

# target2:
# 	$(PYTHON) script2.py

# Targets and Commands
.PHONY: all
all: target1 target2

target1:
	bash mlflow server

target2:
	bash prefect server