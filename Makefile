style:
	flake8 .

tests:
	python manage.py test

check:
	make style
	make tests
