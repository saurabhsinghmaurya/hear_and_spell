FROM python:3.9.10

RUN python -m pip install django

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY spell /code/

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata 20k.json

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
