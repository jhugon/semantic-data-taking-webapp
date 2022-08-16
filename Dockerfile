# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /app

RUN useradd semweb
RUN mkdir -p /home/semweb
RUN chown semweb:semweb /app
RUN chown semweb:semweb /home/semweb

# have to do this here to still be root and before pipenv
COPY Pipfile .
COPY Pipfile.lock .
COPY flask-simple-login flask-simple-login
RUN chown -R semweb:semweb flask-simple-login Pipfile Pipfile.lock

USER semweb
ENV HOME=/home/semweb
ENV PATH="$HOME/.local/bin:$PATH"
RUN echo $PATH

RUN ls -l $HOME
RUN ls -l .
RUN ls -l flask-simple-login

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv sync

# Do this after pip so earlier steps can be cached by Docker
COPY ontology ontology
COPY templates templates
COPY db.py .
COPY web.py .

EXPOSE 8000

CMD ["pipenv","run","gunicorn","-w","1","-b", "0.0.0.0", "web:create_app()"]
