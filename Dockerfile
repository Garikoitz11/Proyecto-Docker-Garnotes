FROM python:3.11-alpine

RUN apk update && apk upgrade --no-cache

WORKDIR /code

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers openldap-dev

COPY requirements.txt /code

RUN pip install -r requirements.txt

EXPOSE 5000 

COPY app.py /code
COPY templates /code/templates

CMD flask run
