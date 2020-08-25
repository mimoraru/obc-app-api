# obc-app-api

## Setup the project

### After building the docker file
```bash
$ sudo docker build .
```

### After building the docker-compose.yml
```bash
$ sudo docker-compose build
```

## TDD 
### run the unit test inside the docker image
Run unit tests for every API feature of developed
To run the test inside docker-composed run in the terminal: 

```bash
$ sudo docker-compose run app sh -c "python manage.py test"
``` 

## Create the core app
```bash
$ sudo docker-compose run app sh -c "python manage.py startapp core"
```

### Create the user model
Run our DB migrations which will create the instructions for Django to create the model in the real DB that we are going to use.
Everytime we make a change to the model we need to run the migrations again. It should create another migrations.py file under migrations. 

```bash
$ sudo docker-compose run app sh -c "python manage.py makemigrations core"
```
Moved to the past commit