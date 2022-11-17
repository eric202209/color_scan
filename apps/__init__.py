from flask import Flask
from flask_migrate import Migrate
from extentions import db
from settings import Config

def create_app():
    app = Flask(__name__,
                static_url_path='',
                static_folder='../app/static',
                template_folder='../app/templates')
    app.config.from_object(Config)

    # 初始化db
    db.init_app(app=app)

    Migrate(app, db)

    return app