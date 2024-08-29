from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "2JTtpCfG6WSqX0ARpTPg6DBM0CqGGKM5" 
jwt = JWTManager(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/real_estate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key

db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))
    role = db.Column(db.String(20), nullable=False, default='user')

    def check_password(self, password):
        print(self.password_hash)
        return check_password_hash(pwhash=self.password_hash, password=password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(self.password_hash)

# Property model
class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Numeric(3, 1))
    square_footage = db.Column(db.Numeric(8, 2))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    offers = db.relationship('Offer', backref='property', lazy=True)
    image_urls = db.Column(JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'price': float(self.price),
            'bedrooms': self.bedrooms,
            'bathrooms': float(self.bathrooms) if self.bathrooms else None,
            'square_footage': float(self.square_footage) if self.square_footage else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_urls': self.image_urls
        }

# Offer model
class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'user_id': self.user_id,
            'amount': float(self.amount),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

# SavedProperty model
class SavedProperty(db.Model):
    __tablename__ = 'saved_properties'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    saved_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def load_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['email'].split('@')[0]
    user = User(username=username, email=data['email'])
    print(data['password'])
    user.set_password(data['password'])
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    print(data['password'])
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    current_user = load_user(current_user_id)
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        # "properties": [sp.property.to_dict() for sp in current_user.saved_properties]
    })

@app.route('/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify([property.to_dict() for property in properties])

@app.route('/properties/<int:id>', methods=['GET'])
def get_property(id):
    property = Property.query.get(id)
    if not property:
        return jsonify({"error": "Property not found"}), 404
    return jsonify(property.to_dict())

@app.route('/properties', methods=['POST'])
@jwt_required()
def add_property():
    data = request.json
    new_property = Property(
        address=data['address'],
        price=data['price'],
        bedrooms=data['bedrooms'],
        bathrooms=data['bathrooms'],
        square_footage=data['square_footage'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        image_urls=data.get('image_urls')
    )
    db.session.add(new_property)
    try:
        db.session.commit()
        return jsonify(new_property.to_dict()), 201
    except:
        db.session.rollback()
        return jsonify({"error": "Failed to add property"}), 400

@app.route('/properties/<int:id>/save', methods=['POST'])
@jwt_required()
def save_property(id):
    current_user_id = get_jwt_identity()
    user = load_user(current_user_id)
    property = Property.query.get(id)
    if not property:
        return jsonify({"error": "Property not found"}), 404
    saved_property = SavedProperty(user_id=user.id, property_id=id)
    db.session.add(saved_property)
    try:
        db.session.commit()
        return jsonify({"message": "Property saved successfully"}), 201
    except:
        db.session.rollback()
        return jsonify({"error": "Failed to save property"}), 400

@app.route('/saved_properties', methods=['GET'])
@jwt_required()
def get_saved_properties():
    current_user_id = get_jwt_identity()
    user = load_user(current_user_id)
    saved_properties = SavedProperty.query.filter_by(user_id=user.id).all()
    properties = [Property.query.get(sp.property_id).to_dict() for sp in saved_properties]
    return jsonify(properties)

@app.route('/properties/<int:id>/offers', methods=['POST'])
@jwt_required()
def submit_offer(id):
    current_user_id = get_jwt_identity()
    current_user = load_user(current_user_id)
    property = Property.query.get(id)
    if not property:
        return jsonify({"error": "Property not found"}), 404
    data = request.json
    new_offer = Offer(
        property_id=id,
        user_id=current_user.id,
        amount=data['amount']
    )
    db.session.add(new_offer)
    try:
        db.session.commit()
        return jsonify(new_offer.to_dict()), 201
    except:
        db.session.rollback()
        return jsonify({"error": "Failed to submit offer"}), 400

@app.route('/offers', methods=['GET'])
@jwt_required()
def get_user_offers():
    current_user_id = get_jwt_identity()
    current_user = load_user(current_user_id)
    offers = Offer.query.filter_by(user_id=current_user.id).all()
    return jsonify([offer.to_dict() for offer in offers])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)