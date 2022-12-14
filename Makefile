DOCKER_SATTAROV_SCHOOL_API_PROJECT := betuple-api-project
DOCKER_SATTAROV_SCHOOL_API_IMAGE_VERSION := 0.0.1
DOCKER_SATTAROV_SCHOOL_API_IMAGE_NAME := cooleekova/first_betuple
DOCKER_SATTAROV_SCHOOL_API_DB_DATA_PATH := /src/docker/betuple-api-db-data
DOCKER_SATTAROV_SCHOOL_API_DB_NAME := betuple
DOCKER_SATTAROV_SCHOOL_API_DB_USERNAME := betuple
DOCKER_SATTAROV_SCHOOL_API_DB_PASSWORD := 14091989

.PHONY: dev-sattarov-school-api-run
dev-sattarov-school-api-run:
	DOCKER_APP_IMAGE_VERSION=$(DOCKER_SATTAROV_SCHOOL_API_IMAGE_VERSION) \
	DOCKER_APP_IMAGE_NAME=$(DOCKER_SATTAROV_SCHOOL_API_IMAGE_NAME) \
	DOCKER_APP_DB_DATA_PATH=$(DOCKER_SATTAROV_SCHOOL_API_DB_DATA_PATH) \
	DOCKER_APP_DB_USERNAME=$(DOCKER_SATTAROV_SCHOOL_API_DB_USERNAME) \
	DOCKER_APP_DB_PASSWORD=$(DOCKER_SATTAROV_SCHOOL_API_DB_PASSWORD) \
	DOCKER_APP_DB_DATABASE=$(DOCKER_SATTAROV_SCHOOL_API_DB_NAME) \
	docker-compose -p $(DOCKER_SATTAROV_SCHOOL_API_PROJECT) -f docker-compose.yaml up -d

.PHONY: dev-sattarov-school-api-image-build
dev-sattarov-school-api-image-build:
	docker build -t $(DOCKER_SATTAROV_SCHOOL_API_IMAGE_NAME):$(DOCKER_SATTAROV_SCHOOL_API_IMAGE_VERSION) .

.PHONY: dev-sattarov-school-api-image-push
dev-sattarov-school-api-image-push:
	docker push $(DOCKER_SATTAROV_SCHOOL_API_IMAGE_NAME):$(DOCKER_SATTAROV_SCHOOL_API_IMAGE_VERSION)

.PHONY: dev-sattarov-school-api-down
dev-sattarov-school-api-down:
	DOCKER_APP_IMAGE_VERSION=$(DOCKER_SATTAROV_SCHOOL_API_IMAGE_VERSION) \
	DOCKER_APP_IMAGE_NAME=$(DOCKER_SATTAROV_SCHOOL_API_IMAGE_NAME) \
	DOCKER_APP_DB_DATA_PATH=$(DOCKER_SATTAROV_SCHOOL_API_DB_DATA_PATH) \
	DOCKER_APP_DB_USERNAME=$(DOCKER_SATTAROV_SCHOOL_API_DB_USERNAME) \
	DOCKER_APP_DB_PASSWORD=$(DOCKER_SATTAROV_SCHOOL_API_DB_PASSWORD) \
	DOCKER_APP_DB_DATABASE=$(DOCKER_SATTAROV_SCHOOL_API_DB_NAME) \
	docker-compose -p $(DOCKER_SATTAROV_SCHOOL_API_PROJECT) down
