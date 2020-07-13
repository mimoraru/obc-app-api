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
I created a simple unit test to test the add function on calc.py 
To run the test inside docker-composed run in the terminal: 

```bash
$ sudo docker-compose run app sh -c "python manage.py test"
``` 

