# Makefile

# Variables
DC=docker-compose
DC_RUN=$(DC) run --rm app sh -c

# Commands
.PHONY: help create-and-run-migrations migrate createmigration run-server superuser shell docker-build docker-up docker-down update test create-project create-app
		help docker-start-service docker-stop-service
default: help

docker-start-service:
	@echo "Starting docker service..."
	@sudo service docker start
dss: docker-start-service

docker-stop-service:
	@echo "Stopping docker service..."
	@sudo service docker stop
dds: docker-stop-service

create-and-run-migrations:
	@echo "Creating and running migrations..."
	$(DC_RUN) "python manage.py makemigrations && python manage.py migrate"
crm: create-and-run-migrations

migrate:
	@echo "Running migrations..."
	$(DC_RUN) "python manage.py migrate"
m: migrate

createmigration:
	@echo "Creating migrations..."
	$(DC_RUN) "python manage.py makemigrations"
cm: createmigration

run-server:
	@echo "Running server..."
	$(DC_RUN) "python manage.py runserver"
r: run-server

superuser:
	@echo "Creating superuser..."
	$(DC_RUN) "python manage.py createsuperuser"
su: superuser

shell:
	@echo "Running shell..."
	$(DC_RUN) "python manage.py shell"
sh: shell

docker-build:
	@echo "Building docker image..."
	$(DC) build
build: docker-build

docker-up:
	@echo "Running docker containers..."
	$(DC) up
up: docker-up

docker-down:
	@echo "Stopping docker containers..."
	$(DC) down
down: docker-down

update: makemigrations docker-build

test:
	@echo "Running tests..."
	$(DC_RUN) "python manage.py test && flake8 --max-line-length=120"
t: test

create-project:
ifeq ($(filter-out $@,$(MAKECMDGOALS)),)
	@echo "Please provide a project name"
else
	@echo "Creating project..."
	django-admin startproject $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)) .
endif
cp: create-project

create-app:
ifeq ($(filter-out $@,$(MAKECMDGOALS)),)
	@echo "Please provide an app name"
else
	@echo "Creating app..."
	$(DC_RUN) "python manage.py startapp $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))"
endif
ca: create-app

# Help
help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  crm, create-and-run-migrations  Create and run migrations"
	@echo "  m, migrate                      Run migrations"
	@echo "  cm, createmigration             Create migrations"
	@echo "  r, run-server                   Run server"
	@echo "  su, superuser                   Create superuser"
	@echo "  sh, shell                       Run shell"
	@echo "  u, update                       Make migrations and and rebuild docker image"
	@echo "  build                           Build docker image"
	@echo "  up                              Run docker containers"
	@echo "  down                            Stop docker containers"
	@echo "  t, test                         Run tests"
	@echo "  cp, create-project              Create project"
	@echo "  ca, create-app                  Create app"
	@echo "  help                            Show this help message and exit"
	@echo ""
	@echo "Examples:"
	@echo "  make crm"
	@echo "  make m"
	@echo "  make cm"
	@echo "  make r"
	@echo "  make su"
	@echo "  make sh"
	@echo "  make u"
	@echo "  make build"
	@echo "  make up"
	@echo "  make down"
	@echo "  make t"
	@echo "  make cp <project_name>"
	@echo "  make ca <app_name>"
	@echo "  make help"
