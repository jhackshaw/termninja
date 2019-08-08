FROM jhackshaw/termninja-base:latest

WORKDIR /app

RUN \
  apk --update add --no-cache --virtual build-deps build-base gcc && \
  pip install bleach python-slugify uvloop==0.13.0rc1 && \
  apk --purge del build-deps

COPY . .

ENTRYPOINT [ "python", "app.py" ]
