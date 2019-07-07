FROM termninja_core


WORKDIR /api
COPY . /api

EXPOSE 8080

CMD ["python", "-m", "sanic", "api.app", "--port=3000", "--host=0.0.0.0", "--debug"]
