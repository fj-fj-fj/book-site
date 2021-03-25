### Book store
#
###### Featuring drf and Oauth

*(Books have authors and readers, price and discounts, rating and likes)*
#
### Usage
```bash
git clone https://github.com/fj-fj-fj/djangoREST-book-site.git
cd djngoREST-book-site
```
#### With Docker  :smiley:
```bash
docker-compose up --build
```

#### Or running natively  :neutral_face:
```pgsql
sudo -u postgres psql
postgres=# create database myproject;
postgres=# create user djangouser with encrypted password 'djangopassword';
postgres=# alter user djangouser createdb;
postgres=# grant all privileges on database myproject to djangouser;
postgres=# \q
```
```python
# Set your config db (djangoREST-book-site/core/settings.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'djangouser',
        'PASSWORD': 'djangopassword',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
```
```bash
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
