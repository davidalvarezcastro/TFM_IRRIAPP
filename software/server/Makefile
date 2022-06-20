# ****************************************************
# * Fichero con funciones directas sobre el proyecto *
# ****************************************************
include .env
export

VENV_NAME ?= venv

PYTHON=$(VENV_NAME)/bin/python3.7
WSGI_PATH=$(subst /,\\/,$(shell sh -c "readlink -f venv/bin")/gunicorn)
GUNICORN_CONFIG=$(subst /,\\/,$(shell sh -c "readlink -f .")/gunicorn.conf.py)
WORKING_PATH=$(subst /,\\/,$(shell sh -c "readlink -f ."))

SERVICES_PATH=/etc/systemd/system
SERVICE_TEMPLATE_FILE=service.service
SERVICE_FILE=servicio_usuarios_tokens.service
USER_NAME=$(subst /,\\/,$(shell sh -c "echo ${USER}"))

SERVICE_FILE_WSGI_PATH_VAR=\$$WSGI_PATH
SERVICE_FILE_SRC_VAR=\$$WSGI_SRC
SERVICE_FILE_USER_VAR=\$$USER
SERVICE_WORKINGPATH_VAR=\$$WORKING_PATH


# TAGS
.PHONY: help
.DEFAULT:= help


# HELP
help:  ## Lista de comandos con su descripcion     
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


virtualenv: ## Crear entorno virtual con sus dependencias
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

dependencies:  ## Actualizar archivo dependencias (requirements.txt)
	pipreqs --force .

install_req:  ## Instalar dependencias definidas en requirements.txt
	. venv/bin/activate && pip install -r requirements.txt


# Api
tests:  ## Ejecutar los tests definidos
	. venv/bin/activate && python manage.py test

run:  ## Iniciar la aplicación - API
	. venv/bin/activate && python manage.py run


# Base de Datos
db_init:  ## Iniciar la base de datos (CUIDADO!!)
	. venv/bin/activate && python manage.py db_init

db_evolve:  ## Permite visualizar las diferencias entre modelos/base de datos (y ejecutar los cambios modelos --> database)
	. venv/bin/activate && python manage.py evolve

db_migration:  ## Generar una migración de la base de datos
	. venv/bin/activate && python manage.py generate_migrate

db_migrate:  ## Ejecuta las migraciones generadas
	. venv/bin/activate && python manage.py migrate

db_models:  ## Obtenemos las tablas de la base de datos a modelos en python
	. venv/bin/activate && python manage.py db_models


# Service (sistema)
init-service: ## Configura e inicia el paquete (api usuarios) como un servicio en el sistema.
	@touch conf/${SERVICE_FILE}
	@sed -e "s/${SERVICE_FILE_WSGI_PATH_VAR}/${WSGI_PATH}/g; \
			 s/${SERVICE_FILE_USER_VAR}/${USER_NAME}/g; \
			 s/${SERVICE_WORKINGPATH_VAR}/${WORKING_PATH}/g; \
			 s/${SERVICE_FILE_SRC_VAR}/${GUNICORN_CONFIG}/g" conf/${SERVICE_TEMPLATE_FILE} > conf/${SERVICE_FILE}

ifeq ("$(wildcard ${SERVICES_PATH}/${SERVICE_FILE})","")
	@sudo ln -s $(shell sh -c "readlink -f conf/${SERVICE_FILE}") ${SERVICES_PATH}/${SERVICE_FILE}
else
	@sudo systemctl daemon-reload
endif
	@sudo systemctl start $(SERVICE_FILE) | cut -d '.' -f1


# Deploy
deploy-docker-db: ## Inicia los contenedores asociados al proyecto
ifeq ($(USERS_DB_DOCKER), 1)
	@docker-compose up -d db
endif


deploy-init: ## Inicia los componentes necesarios (en la api se comprueba si se lanza mediante docker)
	@docker-compose down
	@sudo systemctl stop $(SERVICE_FILE) | cut -d '.' -f1

	@make deploy-docker-db

ifeq ($(USERS_API_DOCKER), 0)
	@make init-service
	@docker-compose up -d nginx
else
	@docker-compose up -d service-oauth-users
endif

