.PHONY: help build up down logs shell test run-tests clean

help:
	@echo "Available commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make up         - Start containers"
	@echo "  make down       - Stop containers"
	@echo "  make logs       - Show logs"
	@echo "  make shell      - Enter container shell"
	@echo "  make test       - Run tests in container"
	@echo "  make run-tests  - Run all tests in container with verbose output"
	@echo "  make clean      - Clean up containers and images"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web /bin/bash

test:
	docker-compose exec web pytest

run-tests:
	docker-compose exec web pytest -v --tb=short --color=yes

clean:
	docker-compose down -v
	docker system prune -f

# Production
build-prod:
	docker build -t ai-agent:latest .

up-prod:
	docker-compose -f docker-compose.prod.yml up -d

down-prod:
	docker-compose -f docker-compose.prod.yml down