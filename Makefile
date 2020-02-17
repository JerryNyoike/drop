venv:
	source venv/bin/activate

env:
	export FLASK_APP=app && export FLASK_ENV=development

serve:
	flask run
