from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    creator = db.Column(db.String(32))
    assignee = db.Column(db.String(32), index=True)
    status = db.Column(db.String(32))

    date_created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    update_time = db.Column(db.DateTime)
    plan_endtime = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='comments', lazy='dynamic')

    def __repr__(self):
        return '<Task {}>'.format(self.id)

    """
    db相关命令创建数据库(在没有使用flask-migrate时使用)
        在python终端 from app import db
                    db.create_all()
                    exit()

    """


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'))

    def __repr__(self):
        return '{}'.format(self.body)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<user:{}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
