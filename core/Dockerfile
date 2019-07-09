FROM python:3.7.3-alpine

ARG editable

WORKDIR /core

RUN \
  apk --update add --no-cache postgresql-libs && \
  apk --update add --no-cache --virtual build-deps build-base wget musl-dev gcc postgresql-dev && \
  pip install setuptools wheel databases sqlalchemy asyncpg sanic sanic-jwt alembic psycopg2 passlib bleach && \
  apk --purge del build-deps

COPY . /core

RUN if [[ -n "$editable" ]]; then pip install -e .; else pip install .; fi
