FROM python:3.7.3-alpine

WORKDIR /app
COPY requirements.txt /app

# RUN apk --update add python py-pip openssl ca-certificates
RUN \
  apk --update add --no-cache postgresql-libs && \
  apk --update add --no-cache --virtual build-deps python-dev build-base wget musl-dev gcc postgresql-dev && \
  pip install -r requirements.txt && \
  apk --purge del build-deps

COPY . /app

EXPOSE 8080

CMD ["/bin/sh", "./entrypoint.sh"]
