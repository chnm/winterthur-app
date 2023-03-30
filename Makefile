preview :
	poetry run python3 manage.py runserver

# Compile TailwindCSS
tailwind :
	poetry run python3 manage.py tailwind start

mm :
	poetry run python3 manage.py makemigrations

migrate :
	poetry run python3 manage.py migrate

graph_illustrate :
	poetry run python3 manage.py graph_models -a -g -o models.png

.PHONY : preview tailwind graph_illustrate
