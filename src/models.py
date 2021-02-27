from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_userid = db.Column(db.Integer, db.ForeignKey("User.id"))
    name = db.Column(db.String(80))
    object_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_userid": self.user_userid,
            "object_id": self.object_id,            
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    skin_color = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    homeworld = db.Column(db.String(80), unique=False, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    # done = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "name": self.name,
            "homeworld": self.homeworld,
            "url": self.url            
            # do not serialize the password, its a security breach
        }
        
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    surface_water = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)
    # done = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "name": self.name,
            "url": self.url,
           
            # do not serialize the password, its a security breach
        }