from extentions import db
import datetime


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.String(50), unique=True)
    display_name = db.Column(db.String(255))
    picture_url = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return 'User:%s' % self.name

    def __init__(self, line_id, display_name='', picture_url=0):
        self.line_id=line_id
        self.display_name=display_name
        self.picture_url=picture_url

    def __str__(self):
        return

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def find_by_name(cls, name):
        return cls.filter_by(name == name).first()
