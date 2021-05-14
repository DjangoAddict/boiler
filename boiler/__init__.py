# this containts the app factory and tells python the directory should be treated as a package

import os
from flask import Flask

from .blueprints.auth import auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)# creates flask instance.  
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'boiler.sqlite'),
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # import db.
    from . import db

    # import blueprints
    # from boiler.blueprints.auth import auth
    # from boiler.blueprints.blog import blog

    # initiate db
    db.init_app(app)

    # register apps
    app.register_blueprint(auth)
    # app.register_blueprint(blog)
    # you can add URL prefixes here or in blueprint.  I prefer here so they are all seen in one place.
    # app.add_url_rule('/', endpoint='index')

    return app