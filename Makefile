.PHONY: all format lint test cov

all: format lint cov

format:
	@echo Format Python code
	black --exclude '/(\.direnv|\.pyenv|venv)/' .
	isort --skip-glob .pyenv --skip-glob venv --profile black .

lint:
	@echo Lint Python code
	flake8 --exclude=.pyenv/,.direnv/,venv/ --ignore=E203,E501,W503
	isort --check-only --skip-glob .pyenv --skip-glob venv --profile black .
	black --check --exclude '/(\.direnv|\.pyenv|venv)/' .

test:
	python -Wall manage.py test

cov:
	coverage run --source='.' --omit '.pyenv/*' manage.py test
	coverage report -m
