# NLP Pipeline

![image](https://github.com/bsenst/mlops/assets/8211411/10d8314c-320a-49f6-91c8-1153e62cd74d)

# Project Criteria
* Problem description
    * [x] Problem is not described (0 points)
    * [ ] Problem is described but shortly or not clearly (1 point)
    * [ ] Problem is well described and it's clear what the problem the project solves (2 points)
* Cloud
    * [ ] Cloud is not used, things run only locally (0 points)
    * [x] The project is developed on the cloud OR the project is deployed to Kubernetes or similar container management platforms (2 points)
    * [ ] The project is developed on the cloud and IaC tools are used for provisioning the infrastructure (4 points)
* Experiment tracking and model registry
    * [ ] No experiment tracking or model registry (0 points)
    * [x] Experiments are tracked or models are registred in the registry (2 points)
    * [ ] Both experiment tracking and model registry are used (4 points)
* Workflow orchestration
    * [ ] No workflow orchestration (0 points)
    * [x] Basic workflow orchestration (2 points)
    * [ ] Fully deployed workflow (4 points)
* Model deployment
    * [ ] Model is not deployed (0 points)
    * [ ] Model is deployed but only locally (2 points)
    * [x] The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used (4 points)
* Model monitoring
    * [x] No model monitoring (0 points)
    * [ ] Basic model monitoring that calculates and reports metrics (2 points)
    * [ ] Comprehensive model monitoring that send alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated (4 points) 
* Reproducibility
    * [x] No instructions how to run code at all (0 points)
    * [ ] Some instructions are there, but they are not complete (2 points)
    * [ ] Instructions are clear, it's easy to run the code, and the code works. The version for all the dependencies are specified. (4 points)
* Best practices
    * [ ] There are unit tests (1 point)
    * [ ] There is an integration test (1 point)
    * [ ] Linter and/or code formatter are used (1 point)
    * [ ] There's a Makefile (1 point)
    * [ ] There are pre-commit hooks (1 point)
    * [ ] There's a CI/CI pipeline (2 points)

# Alternative Data Sources
* https://www.rss-blog.de/das-sind-die-top-nachrichten-rss-feeds-in-deutschland/
