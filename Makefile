build:
	docker build -t specification-subject:latest -f docker/Dockerfile .

up:
	docker-compose --env-file .env -f docker/docker-compose.yaml up -d --build

down:
	docker-compose -f docker/docker-compose.yaml down

stop:
	docker-compose -f docker/docker-compose.yaml stop

restart:
	docker-compose -f docker/docker-compose.yaml down && docker-compose -f docker/docker-compose.yaml up -d --build