SHELL := /bin/bash

.PHONY: up down backend-tests fmt check

up:
	docker compose up --build

down:
	docker compose down

backend-tests:
	cd backend && pytest

fmt:
	npm --prefix frontend run lint

check: backend-tests
