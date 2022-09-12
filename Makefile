.PHONY: all
all: format lint cov

.PHONY: format
format:
	@echo Format Python code
	black --exclude '/(\.direnv|\.pyenv|venv)/' .
	isort --skip-glob .pyenv --skip-glob venv --profile black .

.PHONY: lint
lint:
	@echo Lint Python code
	flake8 --exclude=.pyenv/,.direnv/,venv/ --ignore=E203,E501,W503
	isort --check-only --skip-glob .pyenv --skip-glob venv --profile black .
	black --check --exclude '/(\.direnv|\.pyenv|venv)/' .

.PHONY: test
test:
	python -Wall manage.py test

.PHONY: cov
cov:
	coverage run --source='.' --omit '.pyenv/*' manage.py test
	coverage report -m
