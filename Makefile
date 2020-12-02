SHELL := /bin/bash

migrate:
	docker exec -it backend python ./src/manage.py migrate

makemigrations:
	docker exec -it backend python ./src/manage.py makemigrations

runserver:
	docker exec -it backend python ./src/manage.py runserver 0:9000

collectstatic:
	docker exec -it backend python ./src/manage.py collectstatic --noinput && \
	docker cp backend:/tmp/static_content/static /tmp/static && \
	docker cp /tmp/static nginx:/etc/nginx/static

start:
	cp -n .env.example .env && docker-compose up -d --build

shell:
	docker exec -it backend python ./src/manage.py shell_plus --print-sql

bash:
	docker exec -it backend bash

build: start migrate collectstatic
