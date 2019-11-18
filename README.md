## Install
```sh
pipenv install
```

## Shell
```sh
pipenv shell
```

## Run
```sh
flask run
```

## Task
You will be implementing a very basic passthrough api in flask. It will allow you to "login" as user (no password) get a web token that you use for other API calls. You will pass an API Token and query parameter to the other API. You will implement the following API endpoints.
- POST /login
- GET /user
- GET /widgets