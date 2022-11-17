from flask import Flask
import os

app = Flask(__name__)

class Config:
    SECRET_KEY = os.urandom(32)

    # Enable debug mode
    DEBUG = True
    # 如果設定為True，Flask-SQLAlchemy將跟踪修改並發出信号。默認值為None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))
    # either run on fly or local
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'splite:///'+os.path.join(basedir, 'logs.db')
    if DATABASE_URI.startswith("postgres://"):
        DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    # 設置連接數據庫的URL
    # SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1234@localhost:5432/202210scanner-robot'
    # DATABASE_URI = 'postgresql://admin:1234@localhost:5432/202210scanner-robot'

    # 設置每次請求结束後自動提出數據庫的改動
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 查询时會顯示原始SQL語句
    SQLALCHEMY_ECHO = True


class DevloymentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False