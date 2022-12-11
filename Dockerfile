FROM python:3.9-alpine3.17

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apk add --update --no-cache postgresql-client bash make

RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps
COPY . /code/
