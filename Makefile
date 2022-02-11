.PHONY: format lint test cov

lint:
	flake8 --exclude=.git/,.direnv/ --ignore=E203,E501,W503
	isort --check-only --profile black .
	black --check --exclude '/(\.git|\.direnv)/' .

format:
	black --exclude '/(\.git|\.direnv)/' .
	isort --profile black .

test:
	python -Wall manage.py test

cov:
	coverage run --source='.' --omit '.direnv/*' manage.py test
	coverage report -m
