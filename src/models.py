from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(255), nullable=False)
    
    boards = db.relationship('Board', backref='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def get_id(self):
        return str(self.user_id)


class Board(db.Model):
    __tablename__ = 'boards'

    board_id = db.Column(db.Integer, primary_key=True)
    board_name = db.Column(db.String(80), nullable=False)
    board_description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    lists = db.relationship('CardList', backref='board', cascade='all, delete-orphan')


class CardList(db.Model):
    __tablename__ = 'lists'

    list_id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(80), nullable=False)
    list_position = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.board_id'), nullable=False)

    cards = db.relationship('Card', backref='list', cascade='all, delete-orphan')


class Card(db.Model):
    __tablename__ = 'cards'

    card_id = db.Column(db.Integer, primary_key=True)
    card_title = db.Column(db.String(80), nullable=False)
    card_description = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    importance = db.Column(db.Enum('low', 'medium', 'high'), nullable=False)
    card_position = db.Column(db.Integer, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'), nullable=False)