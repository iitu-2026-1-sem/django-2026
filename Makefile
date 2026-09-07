.PHONY: dev test lint check migrate superuser
dev:
	python manage.py runserver
migrate:
	python manage.py makemigrations && python manage.py migrate
superuser:
	python manage.py createsuperuser
lint:
	ruff check . && ruff format --check .
fmt:
	ruff format . && ruff check --fix .
test:
	pytest -q
check: lint test
