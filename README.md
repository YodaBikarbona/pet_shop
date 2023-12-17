# Pet Shop application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/YodaBikarbona/pet_shop.git
$ cd pet_shop
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:

## DB setup

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(venv)$ python manage.py makemigrations
```
```sh
(venv)$ python manage.py migrate
```

## Run server
```sh
(venv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

## Doc/Redoc

Once the server started use route `api/doc` or `api/redoc`


## Tests

To run the tests, `cd` into the directory where `manage.py` is:
- specific app tests
```sh
(venv)$ python manage.py test animal
```
- all project tests
```sh
(venv)$ python manage.py test
```

