default: full
pwd = $(shell pwd)

stop:
	echo 'Clean dangling images, volumes and containers'
	docker-compose -f sensors/docker-compose.yml down
	docker stack rm prom
	docker images -qf dangling=true | xargs -r docker image rm -f
	docker volume ls -qf dangling=true | xargs -r docker volume rm -f
	# docker rm -v $(shell docker ps -a -q -f status=exited)
	#docker ps --filter status=dead --filter status=exited -aq | xargs -r docker rm -v
run:
	docker build -t hojland/es_indexer:latest $(pwd)/es_indexer
	HOSTNAME=$$(hostname) docker stack deploy -c docker-stack.yml prom
	docker-compose -f sensors/docker-compose.yml up --build -d
full:
	make stop
	sleep 10
	make run