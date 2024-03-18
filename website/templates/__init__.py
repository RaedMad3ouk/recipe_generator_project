from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .views import preference_bp, views


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, static_folder='../static',
                template_folder='../templates')
    app.register_blueprint(views)
    app.register_blueprint(preference_bp, url_prefix='/select')
    app.config['SECRET_KEY'] = 'raedmad3ouk'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')
