all:
	docker build -t spell .

test:
	python3 spell/manage.py test