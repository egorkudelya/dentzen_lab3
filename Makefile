install:
	pip install -r requirements.txt

shell:
	docker-compose -f docker-compose.yml build && \
	docker-compose -f docker-compose.yml run --rm -u 1000 --name dentzen_app --service-ports app bash || \
	true && \
	echo Stopping environment... && \
	docker-compose -f docker-compose.yml -p dentzen_app down

start:
	python manage.py runserver 0.0.0.0:8000
