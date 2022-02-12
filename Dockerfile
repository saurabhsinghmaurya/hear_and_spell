FROM python:3.9.10

RUN python -m pip install django

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY spell /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
