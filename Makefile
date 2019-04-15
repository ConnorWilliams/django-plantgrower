
# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

NAMESPACE := $(if $(NAMESPACE),$(NAMESPACE),eggmancw)
ARCHITECTURE := $(if $(ARCHITECTURE),$(ARCHITECTURE),amd64)
APP_NAME := $(if $(APP_NAME),$(APP_NAME),plant_grower)
LATEST_COMMIT := $(shell git rev-parse HEAD)
DOCKER_TAG := $(LATEST_COMMIT)

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -f Dockerfile.$(ARCHITECTURE) -t $(NAMESPACE)/$(APP_NAME):$(DOCKER_TAG) .
	docker tag $(NAMESPACE)/$(APP_NAME):$(DOCKER_TAG) $(NAMESPACE)/$(APP_NAME):$(ARCHITECTURE)
	docker tag $(NAMESPACE)/$(APP_NAME):$(DOCKER_TAG) $(NAMESPACE)/$(APP_NAME):latest

build-nc: ## Build the container without caching
	docker build -f Dockerfile.$(ARCHITECTURE) -t $(NAMESPACE)/$(APP_NAME):$(DOCKER_TAG) --no-cache .
	docker tag $(NAMESPACE)/$(APP_NAME):$(DOCKER_TAG) $(NAMESPACE)/$(APP_NAME):$(ARCHITECTURE)
	docker tag $(NAMESPACE)/$(APP_NAME):$(DOCKER_TAG) $(NAMESPACE)/$(APP_NAME):latest	

push: ## Push the image to dockerhub
	docker push $(NAMESPACE)/$(APP_NAME)

test:
	docker run -d -p 5432:5432 --name test-postgres -e POSTGRES_PASSWORD=123456 -d postgres
	docker run --name PG --rm -i -t eggmancw/plant_grower:first python -Wa manage.py test plantgrower.tests
	docker stop test-postgres
	docker rm test-postgres