FROM python:3.7.3-alpine

WORKDIR /app

RUN \
  apk --update add --no-cache postgresql-libs && \
  apk --update add --no-cache --virtual build-deps build-base wget musl-dev gcc postgresql-dev && \
  pip install setuptools wheel databases sqlalchemy asyncpg && \
  apk --purge del build-deps

COPY . /app

RUN pip install -e .
