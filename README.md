
[![Build Status](https://travis-ci.com/jhackshaw/termninja.svg?branch=master)](https://travis-ci.com/jhackshaw/termninja)
![GitHub last commit](https://img.shields.io/github/last-commit/jhackshaw/termninja)
[![Live Demo](https://img.shields.io/badge/demo-online-green.svg)](https://www.term.ninja)
![GitHub](https://img.shields.io/github/license/jhackshaw/termninja)

# About

Termninja is a collection of networked, termninal games.


### Games

 - **Snake**: notes support
 - **Celebrity Hangman**
 - **Subnet Racer**


### Structure

    .
    ├── README.md
    ├── docker-compose.yml
    ├── .travis.yml
    ├── client.sh
    |
    ├── games/      # contains the actual game servers
    ├── frontent/   # contains the nextJS frontend
    ├── api/        # Sanic app for api access to backend
    └── base/       # database access shared by api and games
    
 
### Built with

- Asyncio
- Sanic
- NextJS
- Docker









