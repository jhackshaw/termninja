![GitHub last commit](https://img.shields.io/github/last-commit/jhackshaw/termninja)
![GitHub](https://img.shields.io/github/license/jhackshaw/termninja)

## About

Termninja is a collection of networked terminal games including:

#### Snake

#### Celebrity Hangman

#### Subnet Racer

## How to play

1. Clone the Repo
   - `git clone https://github.com/jhackshaw/termninja`
   - `cd termninja`
2. Start the environment
   - `docker-compose up --build`
3. Navigate to [localhost](http://localhost) in a browser to view the scoreboard
4. Install the termninja client in your terminal
   - `curl -X GET http://localhost/client -o ./termninja`
   - `chmod +x ./termninja`
5. Use the client to play games
   - `./termninja --help`
   - `./termninja -a` _(anonymous)_
6. View scores in the browser
7. Give others access to the same server to compete together

## Development

### Project Structure

    .
    ├── README.md
    ├── docker-compose.yml
    ├── termninja
    |
    ├── games/      # individual game servers (asyncio)
    ├── frontend/   # NextJS frontend
    ├── api/        # Sanic app for api access to backend
    └── base/       # database access shared by api and games

### Development environment

Starting the environment using the docker-compose.dev.yml file adds support for hot reloading all of the source code and enables more verbose output.

`docker-compose up -f docker-compose.yml -f docker-compose.dev.yml --build`

### Built with

- Python
- Asyncio
- Sanic
- NextJS/React
- Docker
