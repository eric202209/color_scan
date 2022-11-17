from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from apps.models.user import User
from extentions import db

app = Flask(__name__)
db.init_app(app)
db.app = app

# 初始化migrate
# 兩個參數一個是Flask的app, 一個是數據庫db
migrate = Migrate(app, db)
# 設定你的app
manager = Manager(app)
# 設定python manage.py db 來管理models
manager.add_command('db', MigrateCommand)
# 設定python manage.py runserver為啟動server指令
manager.add_command('runserver', Server())

# 設定python manage.py shell為啟動互動式指令shell的指令
@manager.shell
def make_shell_context():
    return dict(app=app, User=User)


if __name__ == '__main__':
    manager.run()