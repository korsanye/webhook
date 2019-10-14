from datetime import datetime
from dateparser import parse

from flask import Flask
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

from .bootstrap import get_or_create_app
from . import config

app = get_or_create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/webhook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print(config.webhook_expire)
print(parse(config.webhook_expire) if config.webhook_expire else None)


class RouteModel(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(80), unique=True, nullable=False, index=True)
    creation_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now, index=True)
    expiration_date = db.Column(
        db.DateTime, nullable=False, default=lambda: parse(config.webhook_expire) if config.webhook_expire else None, index=True)

    def __repr__(self):
        return '<Route %r>' % self.path


class CallbackModel(db.Model):
    __tablename__ = 'callbacks'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey(RouteModel.id), index=True)
    headers = db.Column(db.Text, default='{}')
    method = db.Column(db.String(12))
    args = db.Column(db.Text())
    body = db.Column(db.Text())
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    referrer = db.Column(db.Text())
    remote_addr = db.Column(db.String(256))

    def __repr__(self):
        return '<Callback %r>' % self.id
