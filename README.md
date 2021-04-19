# Book site

[![Python](https://img.shields.io/static/v1?label=Python&style=plastic&logofor-the-badge&message=3&color=3776AB&logo=PYTHON)](https://www.python.org/)
[![djangorestframework](https://img.shields.io/badge/django-rest-framework?style=flat&logo=djangorest)](https://www.django-rest-framework.org/)
[![PostgresQL](https://img.shields.io/badge/-PostgreSQL-blue?style=flat&logo=postgresql)](https://www.postgresql.org/)


[![CI](https://github.com/fj-fj-fj/djangoREST-book-site/actions/workflows/test-app.yml/badge.svg)](https://github.com/fj-fj-fj/djangoREST-book-site/actions/workflows/test-app.yml)
[![Updates](https://pyup.io/repos/github/fj-fj-fj/book-site/shield.svg)](https://pyup.io/repos/github/fj-fj-fj/book-site/)
[![codecov](https://codecov.io/gh/fj-fj-fj/book-site/branch/main/graph/badge.svg/token=SNfA1GJF7J)](https://codecov.io/gh/fj-fj-fj/book-site)


###### Featuring drf and Oauth

*(Books have authors and readers, price and discounts, rating and likes)*
#
# Installation
```bash
git clone https://github.com/fj-fj-fj/book-site.git
cd book-site
```
Set your sercrets to `.envrc` :heavy_exclamation_mark: [`Direnv on GitHub`](https://github.com/direnv/direnv)

```bash
# EXAMPLE:

# ./.envrc (echo .envrc >> .gitignore)
export DEBUG=True
export DJANGO_SECRET_KEY=your_django_key
export DJANGO_SETTINGS_MODULE=core.settings
export DJANGO_CONFIGURATION=Dev
export DJANGO_ALLOWED_HOSTS=*
export POSTGRES_DB=postgres
export POSTGRES_HOST=api_db  # =api_db if using Docker else 127.0.0.1
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export DATABASE_URL=postgres://postgres:postgres@${POSTGRES_HOST}:5432/postgres
export SOCIAL_AUTH_GITHUB_KEY=your_api_key
export SOCIAL_AUTH_GITHUB_SECRET=your_api_secret
```
#### Use Docker  :whale:
```bash
docker-compose build --build-arg REQUIREMENT_FILE_NAME=local.txt
docker-compose up
```

#### Or running natively  :gear:
```pgsql
sudo -u postgres psql
postgres=# create database myproject;
postgres=# create user djangouser with encrypted password 'djangopassword';
postgres=# alter user djangouser createdb;
postgres=# grant all privileges on database myproject to djangouser;
postgres=# \q
```

```bash
# a few more steps 😊

# Start postgresql
sudo service postgresql start
# Configure the Python virtual environment
python3 -m venv .venv
# Activate the venv
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Set the manage.py to be executable
chmod +x manage.py
# Run Django migrations
python manage.py migrate
# Run tests
./manage.py test
# Run the dev server
./manage.py runserver
```
You can then access the webapp via [`http://127.0.0.1:8000/book/`](http://127.0.0.1:8000/book/)
