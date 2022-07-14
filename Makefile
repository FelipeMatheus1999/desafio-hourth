run:
	@echo "---> Running server..."
	./manage.py runserver ${path}

migrations:
	@echo "---> Running migrations..."
	./manage.py makemigrations

migrate:
	@echo "---> Running migrate..."
	./manage.py migrate