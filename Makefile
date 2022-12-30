app_shell:
	docker-compose -f docker-compose.yml build && \
	docker-compose -f docker-compose.yml run --rm -u 1000 --name dentzen_app --service-ports app bash || \
	true && \
	echo Stopping environment... && \
	docker-compose -f docker-compose.yml -p dentzen_app down

comments_shell:
	docker-compose -f docker-compose.yml build && \
	docker-compose -f docker-compose.yml run --rm -u 1000 --name dentzen_comments --service-ports comments bash || \
	true && \
	echo Stopping environment... && \
	docker-compose -f docker-compose.yml -p dentzen_comments down

install:
	pip install -r requirements.txt

app_start:
	python main/manage.py runserver 0.0.0.0:8000

comments_start:
	python comments/manage.py runserver 0.0.0.0:9000