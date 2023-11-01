from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(250), unique=True, primary_key=True)
    diameter = db.Column(db.Float, unique=False, nullable=True)
    rotation_period = db.Column(db.Float, unique=False, nullable=True)
    gravity = db.Column(db.Float, unique=False, nullable=True)
    climate = db.Column(db.String(250), unique=False, nullable=True)
    terrain = db.Column(db.String(250), unique=False, nullable=True)
    surface_water = db.Column(db.String(250), unique=False, nullable=True)
    url = db.Column(db.String(250), unique=True, nullable=False)
    

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True, primary_key=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    mass = db.Column(db.Integer, unique=False, nullable=True)
    hair_color = db.Column(db.String(16), unique=False, nullable=True)
    eye_color = db.Column(db.String(16), unique=False, nullable=True)
    sex = db.Column(db.String(16), unique=False, nullable=True)
    homeworld = db.Column(db.String(250), ForeignKey('planet.url'))
    planet = db.relationship("Planet")
    url = db.Column(db.String(250), unique=True, nullable=False)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_name = db.Column(db.String(250), unique=True, primary_key=True)
    email = db.Column(db.String(250), unique=True, primary_key=True)
    password = db.Column(db.String(250), unique=False, nullable=False)

class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, ForeignKey('character.id'))
    user = db.relationship("User")
    planet = db.relationship("Planet")
    character = db.relationship("Character")

