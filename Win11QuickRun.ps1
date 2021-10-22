venv\Scripts\activate
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
py -m flask init-db
py -m flask run

pause