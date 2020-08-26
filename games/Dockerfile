FROM termninja_base:latest

WORKDIR /app

RUN \
  apk --update add --no-cache --virtual build-deps build-base gcc && \
  pip install bleach python-slugify uvloop aioredis aiohttp && \
  apk --purge del build-deps

COPY . .

CMD ["python", "run.py"]
