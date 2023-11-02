"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Character, Planet, User, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def handle_people():
    people = Character.query.all()
    results = []
    for person in people:
        serialized = person.serialize()
        results.append({
            "uid": serialized['id'],
            "name": serialized['name'],
            "url": serialized['url']
        })
    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_person(people_id):
    person = Character.query.get(people_id)
    if person != None:
        return jsonify(person.serialize()), 200
    else:
        return jsonify('Invalid person ID.'), 400
        
        
@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planet.query.all()
    results = []
    for planet in planets:
        serialized = planet.serialize()
        results.append({
            "uid": serialized['id'],
            "name": serialized['name'],
            "url": serialized['url']
        })
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet != None:
        return jsonify(planet.serialize()), 200
    else:
        return jsonify('Invalid planet ID.'), 400

@app.route('/users', methods=['GET'])
def handle_users():
    users = User.query.all()
    response_body = []
    for user in users:
        response_body.append(user.serialize())

    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
def handle_user_favorites():
    user = User.query.get(1)
    return jsonify(user.serialize()['favorites']), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_adding_fav_planet(planet_id):
    selected_planet = Planet.query.get(planet_id)
    if selected_planet == None:
        return jsonify("Invalid planet ID."), 400
    else:
        favorite = Favorite(user_id = 1, planet_id = planet_id)
        if Favorite.query.filter_by(planet_id = planet_id).first() == None:
            db.session.add(favorite)
            db.session.commit()
            return jsonify("Favorite added successfully."), 200
        else:
            return jsonify("Favorite already exists"), 400

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def handle_adding_fav_character(character_id):
    selected_character = Character.query.get(character_id)
    if selected_character == None:
        return jsonify("Invalid planet ID."), 400
    else:
        favorite = Favorite(user_id = 1, character_id = character_id)
        if Favorite.query.filter_by(character_id = character_id).first() == None:
            db.session.add(favorite)
            db.session.commit()
            return jsonify("Favorite added successfully."), 200
        else:
            return jsonify("Favorite already exists"), 400
    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def handle_deleting_fav_planet(planet_id):
    favs = Favorite.query.all()
    selected_fav = None
    for fav in favs:
        if fav.serialize()['planet_id'] == planet_id:
            selected_fav = fav
    if selected_fav == None:
        return jsonify("Invalid character ID."), 400
    else:
        db.session.delete(selected_fav)
        db.session.commit()
        return jsonify("Favorite deleted successfully."), 200

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def handle_deleting_fav_character(character_id):
    favs = Favorite.query.all()
    selected_fav = None
    for fav in favs:
        if fav.serialize()['character_id'] == character_id:
            selected_fav = fav
    if selected_fav == None:
        return jsonify("Invalid character ID."), 400
    else:
        #Incomplete
        db.session.delete(selected_fav)
        db.session.commit()
        return jsonify("Favorite deleted successfully."), 200

@app.route('/planet', methods=['POST'])
def handle_add_planet():
    request_data = request.get_json()
    return None

@app.route('/character', methods=['POST'])
def handle_add_character():
    return None

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
