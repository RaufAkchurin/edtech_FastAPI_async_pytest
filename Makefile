up:
	sudo docker-compose -f docker-compose-local.yaml up -d

down:
	sudo docker-compose -f docker-compose-local.yaml down && docker network prune --force

run:
	sudo docker compose -f docker-compose-ci.yaml up -d
