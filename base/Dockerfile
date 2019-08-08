FROM python:3.7.3-alpine

ARG editable

WORKDIR /base

RUN \
  apk --update add --no-cache postgresql-libs && \
  apk --update add --no-cache --virtual build-deps build-base wget musl-dev gcc postgresql-dev && \
  pip install --upgrade pip && \
  pip install setuptools wheel databases sqlalchemy asyncpg alembic psycopg2 passlib && \
  apk --purge del build-deps && \
  rm -rf /var/cache/apk/* && \
  rm -rf /tmp/*

COPY . /base

RUN if [[ -n "$editable" ]]; then pip install -e .; else pip install .; fi
