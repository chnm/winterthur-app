preview :
	poetry run python3 manage.py runserver

# Compile TailwindCSS
tailwind :
	poetry run python3 manage.py tailwind start

mm :
	poetry run python3 manage.py makemigrations

migrate :
	poetry run python3 manage.py migrate

test :
	poetry run python3 manage.py test

# Helpers for loading data
loadlanguages :
	poetry run python manage.py loaddata languages.yaml

loadcollection :
	poetry run python manage.py loaddata collection.yaml

loaddocument :
	poetry run python manage.py importdata --filepath="/Spreadsheet_Sample_2024-02-08.xlsx" --sheetname="Documents"

loadfragments :
	poetry run python manage.py importfragments --filepath="/Spreadsheet_Sample_2024-02-08.xlsx" --sheetname="Fragments"

loadimages :
	poetry run python manage.py importimages


.PHONY : preview tailwind mm migrate test loaddocument loadfragments loadimages
