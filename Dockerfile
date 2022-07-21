# syntax=docker/dockerfile:1
FROM python:3.10

COPY . /app
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pipenv install gunicorn

EXPOSE 8000

CMD ["pipenv","run","gunicorn","-w","4","-b", "0.0.0.0", "web:app"]
