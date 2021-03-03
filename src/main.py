import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites
import datetime

## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

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
#################################################### Users #########################################################
@app.route('/user', methods=['GET'])
def handle_hello():

    # get all the todos
    query = User.query.all()
    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))
    return jsonify(results), 200

@app.route('/add_user', methods=['POST'])
def add_user():
     request_body = json.loads(request.data) #Peticion de los datos, que se cargaran en formato json  // json.loads transcribe a lenguaje de python UTF-8
     if request_body["name"] == None and request_body["email"] == None:
         return "Datos incompletos, favor completar todos los datos!"
     else:
         user = User(name= request_body["name"], email= request_body["email"], password= request_body["password"])
         db.session.add(user)
         db.session.commit()
         return "Posteo Exitoso"

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def del_user_by_id(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return("User has been deleted successfully"), 200
#################################################### Favorites ########################################################
@app.route('/get_favorites', methods=['GET'])
def get_favorites():

    # get all the todos
    query = Favorites.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))

    return jsonify(results), 200
@app.route('/users/get_favorites', methods=['POST'])
def add_fav():
    
    # recibir info del request
    add_new_fav = json.loads(request.data)
    newFav = Favorites(user_id=add_new_fav["userid"], name=add_new_fav["name"], object_id=add_new_fav["object_id"])
    db.session.add(newFav)
    db.session.commit()

    return jsonify("All good"), 200


@app.route('/users/<int:userid>/get_favorites', methods=['GET'])
def get_user_favorite(userid):
    favorites = Favorites.query.filter_by(user_id = userid)
    # favorites = Favorites.query.all()
    # print(favorites)
    results = list(map(lambda x: x.serialize(), favorites))
    # print(results)
    return jsonify(results), 200
    # return jsonify("hola"), 200


@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def del_fav(favorite_id):

    # recibir info del request
    
    delete_favorite = Favorites.query.get(favorite_id)
    if delete_favorite is None:
        raise APIException('Label not found', status_code=404)

    db.session.delete(delete_favorite)
    db.session.commit()

    return jsonify("All good"), 200
#################################################### People ###########################################################
@app.route('/get_characters', methods=['GET'])
def get_characters():

    # get all the todos
    query = Characters.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))

    return jsonify(results), 200
@app.route('/get_characters/<int:chaid>', methods=['GET'])
def handle_character(chaid):

    # get all the todos
    persona = Characters.query.get(chaid)
    # map the results and your list of people  inside of the all_people variable
    return jsonify(persona.serialize()), 200
#Favorites and Users:
# @app.route('/user/<int:userid>/get_favorites', methods=['POST'])
# def add_user_favorite(userid):
#     post_favorites = request.get_json()
#     add_favorites = Favorites(user_userid=userid, object_id = post_favorites["object_id"], name=post_favorites["name"])
#     db.session.add(add_favorites)
#     db.session.commit()
#     return jsonify(result), 200


#################################################### Planets ###################################################################
@app.route('/get_planets', methods=['GET'])
def get_planets():

    # get all the todos
    query = Planets.query.all()

    # map the results and your list of people  inside of the all_people variable
    results = list(map(lambda x: x.serialize(), query))

    return jsonify(results), 200

@app.route('/get_planets/<int:planid>', methods=['GET'])
def handle_planet(planid):

    # get all the todos
    planeta = Planets.query.get(planid)
    # map the results and your list of people  inside of the all_people variable
    return jsonify(planeta.serialize()), 200
################################################### REGISTER ##########################################################
@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "email is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg": "Username  already exists"}), 400

        user = User()
        user.email = email
        hashed_password = generate_password_hash(password)
        print(password, hashed_password)

        user.password = hashed_password

        db.session.add(user)
        db.session.commit()

        return jsonify({"success": "Thanks. your register was successfully", "status": "true"}), 200
############################################## LOGIN ######################################################
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "Username is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        # crear el token
        expiracion = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.email, expires_delta=expiracion)

        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000
        }

        return jsonify(data), 200
################################### PROFILE ####################################################
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if request.method == 'GET':
        token = get_jwt_identity()
        return jsonify({"success": "Acceso a espacio privado", "usuario": token}), 200
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
