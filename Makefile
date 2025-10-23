.PHONY: init up down logs

COMPOSE := docker compose

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

## Initialize the airflow system
init:
	$(COMPOSE) up airflow-init

## Bring up all the containers
up:
	$(COMPOSE) up -d

## Shutdown all the containers
down:
	$(COMPOSE) down

## Tail logs for the project
logs:
	$(COMPOSE) logs -f

## Tail logs for the project
shell:
	$(COMPOSE) exec airflow-worker /bin/bash

## print help message.
help:
		@echo ''
		@echo 'Usage:'
		@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
		@echo ''
		@echo 'Targets:'
		@awk '/^[a-zA-Z\-\_0-9]+:/ { \
				helpMessage = match(lastLine, /^## (.*)/); \
				if (helpMessage) { \
						helpCommand = substr($$1, 0, index($$1, ":")-1); \
						helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
						printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} \n\t${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
				} \
		} \
		{ lastLine = $$0 }' $(MAKEFILE_LIST)

