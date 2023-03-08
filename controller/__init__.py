import os

from decouple import config
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'db.sqlite3'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database
    database.init_app(app)

    from . import authentication
    app.register_blueprint(authentication.blueprint)

    from . import accounts
    app.register_blueprint(accounts.blueprint)

    return app
