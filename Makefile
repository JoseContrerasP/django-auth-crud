# run:
# 	python manage.py runserver --settings=settings.local

# makemigrations:
# 	python manage.py makemigrations --settings=settings.local

# migrate:
# 	python manage.py migrate --settings=settings.local

# activate:
# 	env\scripts\activate

# shell:
# 	python manage.py shell --settings=settings.local

run:
	python manage.py runserver 

makemigrations:
	python manage.py makemigrations 

migrate:
	python manage.py migrate 

shell:
	python manage.py shell 