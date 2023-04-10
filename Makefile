.PHONY: all
all: format lint cov

.PHONY: format
format:
	@echo Format Python code
	black --exclude '/\.venv/' .
	isort --skip-glob .venv --profile black .

.PHONY: lint
lint:
	@echo Lint Python code
	flake8 --exclude=.venv/ --ignore=E203,E501,W503
	isort --check-only --skip-glob venv --profile black .
	black --check --exclude '/\.venv/' .

.PHONY: test
test:
	python -Wall manage.py test

.PHONY: cov
cov:
	coverage run --source='.' manage.py test
	coverage report -m

.PHONY: upgrade
upgrade:
	pip-compile -U requirements.in --resolver=backtracking
	pip install --upgrade pip
	pip install -r requirements.txt
