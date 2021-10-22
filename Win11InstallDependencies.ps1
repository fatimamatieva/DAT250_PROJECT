py -m venv venv
venv\Scripts\activate
py -m pip install Flask
py -m pip install email_validator
py -m pip install flask-talisman
py -m pip install -e ./flask-wtf
py -m flask init-db

pause
