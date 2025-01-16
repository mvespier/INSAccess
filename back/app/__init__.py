from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import URLSafeSerializer
import json

db= SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    # load the instance config, if it exists, when not testing
    if test_config is None:
        config_file_name = "config.json"
    else:
        config_file_name = "test_config.json"

    with open(config_file_name) as json_file:
        config_json = json.load(json_file)
        for k, v in config_json.items():
            app.config[k] = v

    # utilities
    global serializer
    serializer = URLSafeSerializer(app.config['URL_SERIALIZER_SECRET'], salt="chpassword")

    global mail
    mail = Mail(app) 

    #initialize the database
    db.init_app(app)

    #initialize the login manager from Flask
    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'# set the login view to the one defined in auth.py
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from .blueprints.auth import auth as auth_blueprint
    from .blueprints.main import main as main_blueprint
    from .blueprints.parameters import parameters as parameters_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    

    return app