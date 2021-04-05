style:
	flake8 .

tests:
	python manage.py test

security:
	safety check -r requirements/base.txt --full-report

check:
	make style
	make tests
	make security
