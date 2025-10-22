.PHONY: init up down logs

COMPOSE := docker compose

init:
	$(COMPOSE) up airflow-init

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down


logs:
	$(COMPOSE) logs -f
