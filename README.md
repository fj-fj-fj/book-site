# Online Library

[![Python](https://img.shields.io/static/v1?label=Python&style=plastic&logofor-the-badge&message=3&color=3776AB&logo=PYTHON)](https://www.python.org/)
[![djangorestframework](https://img.shields.io/badge/django-rest-framework?style=flat&logo=djangorest)](https://www.django-rest-framework.org/)
[![CI](https://github.com/fj-fj-fj/djangoREST-book-site/actions/workflows/test-app.yml/badge.svg)](https://github.com/fj-fj-fj/djangoREST-book-site/actions/workflows/test-app.yml)


###### Featuring drf and Oauth

*(Books have authors and readers, price and discounts, rating and likes)*
#
# Usage
```bash
git clone https://github.com/fj-fj-fj/djangoREST-book-site.git
cd djngoREST-book-site
```
#### Docker  :whale:
```bash
docker-compose up --build
# postgres:314MB app:176MB
```

#### Or running natively
```pgsql
sudo -u postgres psql
postgres=# create database myproject;
postgres=# create user djangouser with encrypted password 'djangopassword';
postgres=# alter user djangouser createdb;
postgres=# grant all privileges on database myproject to djangouser;
postgres=# \q
```
#### Set your config to `.env`
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
You can then access the webapp via http://127.0.0.1:8000/book/
#
:heavy_exclamation_mark: Add all sercrets into `.envrc` 