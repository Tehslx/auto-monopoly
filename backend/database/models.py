from backend.config.config import *
from backend.database.extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    monopoly_email = db.Column(db.String(120), nullable=True)
    monopoly_password = db.Column(db.String(60), nullable=True)
    proxy = db.Column(db.String(120), nullable=True)
    is_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    bot_enabled = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def is_active(self):
        return self.is_confirmed

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"User('{self.username}')"