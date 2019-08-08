FROM jhackshaw/termninja-base:latest


RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*

RUN apk update

WORKDIR /uvloop

RUN \
  pip install bleach python-slugify uvloop==0.13.0rc1

WORKDIR /app
COPY . .

ENTRYPOINT [ "python", "app.py" ]
