FROM termninja_core

RUN \
  apk --update add --no-cache postgresql-libs && \
  apk --update add --no-cache --virtual build-deps gcc musl-dev build-base postgresql-dev python3-dev && \
  pip install sanic alembic psycopg2 && \
  apk --purge del build-deps

WORKDIR /app
COPY . /app

EXPOSE 8080

CMD ["python", "app"]
