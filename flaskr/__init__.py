import os

from flask import Flask
from logging.config import dictConfig
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_talisman import Talisman
from datetime import timedelta

def create_app(test_config=None):
    # configure logging
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='d5c500689d78aa18776a4b203f1428fc46d47b3e74caf37fb6beb89d9d4a1bc4',
        WTF_CSRF_SECRET_KEY='155c076d61cf82778ececfcca6efbd38a845f66cd323798a2d06d9801ad9c5cb',
        PERMANENT_SESSION_LIFETIME = timedelta(minutes=60),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CSRFProtect(app)
    Talisman(app,
    content_security_policy={
        'font-src': [
            '\'self\'',
            'https://fonts.gstatic.com',
        ],
        'style-src': [
            '\'self\'',
            'https://fonts.googleapis.com',
        ],
    })

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    
    from . import booking
    app.register_blueprint(booking.bp)
    app.add_url_rule('/', endpoint='index')
    cwd = os.getcwd()
    app.run(host='0.0.0.0', port=5000, ssl_context=(cwd+'\cert.pem', cwd+'\key.pem'))

    return app
