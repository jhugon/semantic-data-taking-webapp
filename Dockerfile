# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
COPY flask-simple-login flask-simple-login

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
RUN pipenv install gunicorn

# Do this after pip so earlier steps can be cached by Docker
COPY ontology ontology
COPY templates templates
COPY db.py .
COPY web.py .

EXPOSE 8000

CMD ["pipenv","run","gunicorn","-w","4","-b", "0.0.0.0", "web:app"]
