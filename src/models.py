from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(250), unique=True, primary_key=True)
    diameter = db.Column(db.Float, unique=False, nullable=True)
    rotation_period = db.Column(db.Float, unique=False, nullable=True)
    gravity = db.Column(db.Float, unique=False, nullable=True)
    climate = db.Column(db.String(250), unique=False, nullable=True)
    terrain = db.Column(db.String(250), unique=False, nullable=True)
    surface_water = db.Column(db.String(250), unique=False, nullable=True)
    url = db.Column(db.String(250), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "url": self.url
        }
    

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String, unique=True, primary_key=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    mass = db.Column(db.Integer, unique=False, nullable=True)
    hair_color = db.Column(db.String(16), unique=False, nullable=True)
    eye_color = db.Column(db.String(16), unique=False, nullable=True)
    sex = db.Column(db.String(16), unique=False, nullable=True)
    homeworld = db.Column(db.String(250), db.ForeignKey('planet.url'))
    planet = db.relationship("Planet")
    url = db.Column(db.String(250), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "sex": self.sex,
            "homeworld": self.homeworld,
            "planet": self.planet,
            "url": self.url
        }

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='user')

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "favorites": list(map(lambda x: x.serialize(), self.favorites))
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet = db.relationship("Planet")
    character = db.relationship("Character")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }

