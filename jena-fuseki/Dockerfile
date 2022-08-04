# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y wget tar gzip

WORKDIR /app
RUN wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.5.0.tar.gz
RUN ls -la /root
RUN tar xzf apache-jena-fuseki-4.5.0.tar.gz
RUN ls -la *

RUN apt-get install -y openjdk-11-jdk-headless

RUN ls -la *

EXPOSE 3030

ENV DB_FILE_LOC=/app/db

RUN mkdir -p db

CMD ["./apache-jena-fuseki-4.5.0/fuseki-server","--update","--loc=db","/semweb"]
