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
from models import db, User, Favorites, Characters, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

    # get all the todos
    query = User.query.all()
    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))
    return jsonify(results), 200

@app.route('/get_favorites', methods=['GET'])
def get_favorites():

    # get all the todos
    query = Favorites.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))

    return jsonify(results), 200

@app.route('/get_characters', methods=['GET'])
def get_characters():

    # get all the todos
    query = Characters.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))

    return jsonify(results), 200

@app.route('/get_planets', methods=['GET'])
def get_planets():

    # get all the todos
    query = Planets.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))

    return jsonify(results), 200

@app.route('/get_planets/<int:id>', methods=['GET'])
def handle_planet(id):

    # get all the todos
    vuelta = Planets.query.get(id)
    # map the results and your list of people  inside of the all_people variable
    return jsonify(vuelta.serialize()), 200

@app.route('/get_characters/<int:id>', methods=['GET'])
def handle_character(id):

    # get all the todos
    vuelta = Characters.query.get(id)
    # map the results and your list of people  inside of the all_people variable
    return jsonify(vuelta.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
