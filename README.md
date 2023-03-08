# HedgeDoc Controller

This repository contains the source code for a small website.
The website is used to interact with a HedgeDoc instance and brings 
some convenience features and statistics.
The website is written with flask and uses sqlite as a database.

## Development

Start development webserver:

```shell
flask --app controller run --debug
```

## Management

Initialize database:

```shell
flask --app controller init-db
```

Create a new user:

```shell
flask --app controller auth register <name> <password>
```

## Author

© Aiven Timptner
