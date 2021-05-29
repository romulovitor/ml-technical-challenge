
.ONESHELL:
PYTHON := ${PWD}/venv/bin/python3
PIP := ${PWD}/venv/bin/pip3

.PHONY: up

up:
	docker-compose up

.PHONY: down

down:
	docker-compose down

logs:
	docker-compose logs -f

user:
	docker run -d --network default --name mongo \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    mongo
api:
	docker build -t api .
map:
	docker stop `docker ps -a -q`
rm:
	docker rm `docker ps -a -q`

venv:
	@echo "Inicializa uma venv local."
	virtualenv venv -p python

install: venv
	@echo "Instala as dependências numa venv local."
	${PIP} install -r requirements.txt


#docker stop `docker ps -a -q`
# docker rm `docker ps -a -q`
#docker-compose down --rmi all -v
# mongo -u romulo -p toor
# docker build -t myimage .
# db.links.find().pretty()
# db.links.remove({})