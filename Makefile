all:
	python3 spell/manage.py makemigrations app
	python3 spell/manage.py migrate
	python3 spell/manage.py loaddata spell/20k.json
	docker build -t spell .

test:
	python3 spell/manage.py test