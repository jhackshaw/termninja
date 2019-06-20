FROM shell_games_base

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3000

ENTRYPOINT [ "python", "main.py" ]