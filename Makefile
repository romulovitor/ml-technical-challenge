include .env

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
#docker stop `docker ps -a -q`
# docker rm `docker ps -a -q`
# mongo -u romulo -p toor