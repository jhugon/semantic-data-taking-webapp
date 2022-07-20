FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["web.py"]
