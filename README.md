# chaitinschool.org

Chaitin School of Software Engineering.

## Development

This is a [Django](https://www.djangoproject.com/) codebase. Check out the
[Django docs](https://docs.djangoproject.com/) for general technical
documentation.

### Structure

The Django project is `chaitin`. There is one Django app, `main`, with all
business logic. Application CLI commands are generally divided into two
categories, those under `python manage.py` and those under `make`.

```
├── ...
├── Makefile
├── manage.py
├── chaitin
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main
    ├── ...
    ├── migrations/
    ├── templates/
    ├── static/
    ├── apps.py
    ├── urls.py
    ├── models.py
    └── views.py
```

### Dependencies

Using [venv](https://docs.python.org/3/library/venv.html):

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

This project also uses [pip-tools](https://github.com/jazzband/pip-tools) for
dependency management.

### Serve

To run the Django development server:

```sh
python manage.py runserver
```

## Testing

Using the Django test runner:

```sh
make test
```

For coverage, run:

```sh
make cov
```

## Code linting & formatting

The following tools are used for code linting and formatting:

* [black](https://github.com/psf/black) for code formatting.
* [isort](https://github.com/pycqa/isort) for imports order consistency.
* [flake8](https://gitlab.com/pycqa/flake8) for code linting.

To use:

```sh
make format
make lint
```

## License

This software is licensed under the MIT license. For more information, read the
[LICENSE](LICENSE) file.
