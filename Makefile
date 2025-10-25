SHELL := /bin/bash

.PHONY: up down backend-tests fmt

up:
	docker compose up --build

down:
	docker compose down

backend-tests:
	cd backend && pytest

fmt:
	npm --prefix frontend run lint
