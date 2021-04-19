WSL_CHROME_EXE = "${BROWSER}"
PATH_TO_COVERAGE_INDEX_HTML = ${HTMLCOV}

.PHONY: clean db install install-dev isort help run tests types
.DEFAULT_GOAL : help

help:
	@echo "--------------------------------------HELP----------------------------------------"
	@echo "install-dev - initialize local environement for development. Requires venv"
	@echo "install - install the package to the active Python's site-packages"
	@echo "db - Postgresql start."
	@echo "run - Django runserver."
	@echo "clean - remove all, test, coverage and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "style - check style with flake8"
	@echo "coverage - check code coverage quickly"
	@echo "tests - run Django's unit tests."
	@echo "security - check your installed dependencies for known security vulnerabilities"
	@echo "check - do a full check (style, tests, security)"
	@echo "----------------------------------------------------------------------------------"

check-virtual-env:
	@echo virtual-env: $${VIRTUAL_ENV?"Please run in virtualual environement"}

install-dev: check-virtual-env
	pip install -r requirements/local.txt

install:
	pip install -r requirements.txt
	echo skipping pip install -r requirements/local.txt

run:
	make db
	./manage.py runserver

db:
	service postgresql start

style:
	flake8 .

types:
	mypy .

isort:
	isort .

tests:
	./manage.py test

coverage:
	coverage run --source='.' ./manage.py test .
	coverage report -m
	coverage html
	$(WSL_CHROME_EXE) $(PATH_TO_COVERAGE_INDEX_HTML)

clean: clean-pyc, clean-test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fv ./reports/.coverage
	rm -fv reports/cover/*

security:
	safety check -r requirements/base.txt --full-report

check:
	make isort
	make style
	make types
	make tests
	make security
