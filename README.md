# Dexi

> Automate everything!

### Quick Start

If you want to get up and running with Dexi immediately, run:

```
docker-compose build cli && docker-compose run --rm cli python cli.py dexi dashboard
```

### Getting Started

To build and run the CLI on your host, you will need Python 3.9, pip, and virtualenv to build and run `dexi`:

```bash
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements_dev.txt
(env)$ python cli.py dexi dashboard
```

If you wish to keep a copy of Dexi on your host system forever, you can install and run it using:

```bash
$ pip install -e .
$ dexi dashboard
```

Alternatively, you can use docker to build an image and run that image with all of the necessary dependencies using the following commands:

```bash
$ docker-compose build cli
$ docker-compose run --rm cli python cli.py dexi dashboard
```

### Testing

A test suite has been included to ensure Dexi functions correctly:.

To run the entire test suite with verbose output, run the following:

```bash
$ pytest -vvv
```

Alternatively, to run a single set of tests.

```bash
$ pytest -vvv tests/models/test_delivery.py
```

All tests can be run within docker by using the following command:

```bash
$ docker-compose build pytest && docker-compose run --rm pytest

tests/test_cli.py

----------- coverage: platform linux, python 3.9.0-final-0 -----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
dexi/__init__.py         0      0   100%
------------------------------------------------------
TOTAL                    0      0   100%
```

### Linting

```
docker-compose build
docker-compose run --rm black
docker-compose run --rm flake8
docker-compose run --rm isort
docker-compose run --rm mypy
docker-compose run --rm pylint
```

# Contributions

Please read [CONTRIBUTING.md](.github/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
