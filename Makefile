.PHONY: all
all: format lint cov

.PHONY: format
format:
	@echo Format Python code
	./.venv/bin/black --exclude '/\.venv/' .
	./.venv/bin/isort --skip-glob .venv --profile black .

.PHONY: lint
lint:
	@echo Lint Python code
	./.venv/bin/flake8 --exclude=.venv/ --ignore=E203,E501,W503
	./.venv/bin/isort --check-only --skip-glob venv --profile black .
	./.venv/bin/black --check --exclude '/\.venv/' .

.PHONY: test
test:
	./.venv/bin/python -Wall manage.py test

.PHONY: cov
cov:
	./.venv/bin/coverage run --source='.' manage.py test
	./.venv/bin/coverage report -m

.PHONY: upgrade
upgrade:
	./.venv/bin/pip-compile -U requirements.in
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install -r requirements.txt
