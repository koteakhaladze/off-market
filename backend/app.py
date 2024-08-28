from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/real_estate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key

db = SQLAlchemy(app)
login_manager = LoginManager()

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')
    saved_properties = db.relationship('SavedProperty', backref='user', lazy=True)
    offers = db.relationship('Offer', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'price': float(self.price),
            'bedrooms': self.bedrooms,
            'bathrooms': float(self.bathrooms) if self.bathrooms else None,
            'square_footage': float(self.square_footage) if self.square_footage else None,
            'latitude': self.latitude,
            'longitude': self.longitude
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
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
@login_required
@admin_required
def add_property():
    data = request.json
    new_property = Property(
        address=data['address'],
        price=data['price'],
        bedrooms=data['bedrooms'],
        bathrooms=data['bathrooms'],
        square_footage=data['square_footage'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    db.session.add(new_property)
    try:
        db.session.commit()
        return jsonify(new_property.to_dict()), 201
    except:
        db.session.rollback()
        return jsonify({"error": "Failed to add property"}), 400

@app.route('/properties/<int:id>/save', methods=['POST'])
@login_required
def save_property(id):
    property = Property.query.get(id)
    if not property:
        return jsonify({"error": "Property not found"}), 404
    saved_property = SavedProperty(user_id=current_user.id, property_id=id)
    db.session.add(saved_property)
    try:
        db.session.commit()
        return jsonify({"message": "Property saved successfully"}), 201
    except:
        db.session.rollback()
        return jsonify({"error": "Failed to save property"}), 400

@app.route('/saved_properties', methods=['GET'])
@login_required
def get_saved_properties():
    saved_properties = SavedProperty.query.filter_by(user_id=current_user.id).all()
    properties = [Property.query.get(sp.property_id).to_dict() for sp in saved_properties]
    return jsonify(properties)

@app.route('/properties/<int:id>/offer', methods=['POST'])
@login_required
def submit_offer(id):
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
@login_required
def get_user_offers():
    offers = Offer.query.filter_by(user_id=current_user.id).all()
    return jsonify([offer.to_dict() for offer in offers])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)