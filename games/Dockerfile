FROM jhackshaw/termninja-base:latest


RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*

RUN apk update

WORKDIR /uvloop

# bulild master branch of uvloop
# this should not be necessary once uvloop 0.13 is released
RUN \
  apk --update add --no-cache --virtual uvloop-build-deps build-base wget gcc automake libtool libtool-doc m4 autoconf git && \
  git clone --recursive https://github.com/MagicStack/uvloop && \
  cd uvloop && \
  pip install cython && \
  pip install . && \
  apk --purge del uvloop-build-deps

RUN \
  pip install bleach python-slugify

WORKDIR /app
COPY . .

ENTRYPOINT [ "python", "app.py" ]
