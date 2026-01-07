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
from models import db, User, Character, Planet, Starship, FavoriteCharacter, FavoritePlanet, FavoriteStarship
#from models import Person

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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():
    users= User.query.all()
    print(users)
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    return jsonify({'data': users[0].serialize()})

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    fav_people = []
    for f in user.favorite_characters:
        fav_people.append(f.serialize())

    fav_planets = []
    for f in user.favorite_planets:
        fav_planets.append(f.serialize())

    fav_starships = []
    for f in user.favorite_starships:
        fav_starships.append(f.serialize())

    return jsonify({
        'favorite_people': fav_people,
        'favorite_planets': fav_planets,
        'favorite_starships': fav_starships
    }), 200

@app.route('/character', methods=['POST'])
def add_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'El campo name es obligatorio'}), 400
    if 'height' not in body:
        return jsonify({'msg': 'El campo height es obligatorio'}), 400
    new_character = Character()
    new_character.name = body['name']
    new_character.height = body['height']
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'msg': 'Usuario agregado exitosamente'}), 201

@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()

    people_serialized = []
    for p in people:
        people_serialized.append(p.serialize())

    return jsonify({'data': people_serialized}), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    person = Character.query.get(people_id)

    if person is None:
        return jsonify({'msg': 'Personaje no encontrado'}), 404

    return jsonify({'data': person.serialize()}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()

    planets_serialized = []
    for p in planets:
        planets_serialized.append(p.serialize())

    return jsonify({'data': planets_serialized}), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({'msg': 'Planeta no encontrado'}), 404

    return jsonify({'data': planet.serialize()}), 200

@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):

    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if user is None or planet is None:
        return jsonify({'msg': 'Usuario o planeta no existen'}), 404

    fav = FavoritePlanet()
    fav.user_id = user_id
    fav.planet_id = planet_id

    db.session.add(fav)
    db.session.commit()

    return jsonify({'msg': 'Planeta favorito agregado exitosamente'}), 201


@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):

    fav = FavoritePlanet.query.filter_by(
        user_id=user_id,
        planet_id=planet_id
    ).first()

    if fav is None:
        return jsonify({'msg': 'Planeta favorito no encontrado'}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({'msg': 'Planeta favorito eliminado correctamente'}), 200

@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_people(people_id, user_id):

    user = User.query.get(user_id)
    people = Character.query.get(people_id)

    if user is None or people is None:
        return jsonify({'msg': 'Usuario o personaje no existen'}), 404

    fav = FavoriteCharacter()
    fav.user_id = user_id
    fav.character_id = people_id

    db.session.add(fav)
    db.session.commit()

    return jsonify({'msg': 'People favorito agregado exitosamente'}), 201


@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_people(people_id, user_id):

    fav = FavoriteCharacter.query.filter_by(
        user_id=user_id,
        character_id=people_id
    ).first()

    if fav is None:
        return jsonify({'msg': 'People favorito no encontrado'}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({'msg': 'People favorito eliminado correctamente'}), 200

@app.route('/favorite/starship/<int:starship_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_starship(starship_id, user_id):

    user = User.query.get(user_id)
    ship = Starship.query.get(starship_id)

    if user is None or ship is None:
        return jsonify({'msg': 'Usuario o nave no existen'}), 404

    fav = FavoriteStarship()
    fav.user_id = user_id
    fav.starship_id = starship_id

    db.session.add(fav)
    db.session.commit()

    return jsonify({'msg': 'Nave favorita agregada exitosamente'}), 201


@app.route('/favorite/starship/<int:starship_id>/user/<int:user_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id, user_id):

    fav = FavoriteStarship.query.filter_by(
        user_id=user_id,
        starship_id=starship_id
    ).first()

    if fav is None:
        return jsonify({'msg': 'Nave favorita no encontrada'}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({'msg': 'Nave favorita eliminada correctamente'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
