FROM termninja_base

RUN \
  apk --update add --no-cache --virtual build-deps build-base gcc && \
  pip install sanic sanic-jwt sanic-cors && \
  apk --purge del build-deps

WORKDIR /api
COPY . /api

EXPOSE 8080

RUN alembic upgrade head

CMD ["python", "run.py"]
