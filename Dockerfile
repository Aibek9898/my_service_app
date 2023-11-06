#основной образ(image)
FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user
RUN chown service-user:service-user -R /service/

USER service-user

