from flask import Blueprint, request, jsonify, current_app, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import logging

bp = Blueprint('auth', __name__, url_prefix='/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.get_by_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()


    if not all(key in data for key in ('first_name', 'last_name', 'email', 'password', 'role')):
        return jsonify({'message': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(data['password'])
    
    try:

        new_user = User.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password,
            role=data['role'],
            phone=data.get('phone'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            address=data.get('address')
        )
        
    
        if new_user:
            return jsonify({'message': 'User created successfully'}), 201
        else:
            logging.warning("User creation returned None.")
            return jsonify({'message': 'User creation failed'}), 500

    except Exception as e:
        logging.error(f"Error during user creation: {str(e)}")
        return jsonify({'message': str(e)}), 400


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    logging.info(f"Received login request for: {data['first_name']}")
    
    user = User.get_by_username(data['first_name'])
    
    if user:
        logging.info(f"User retrieved: {user.first_name}, {user.email}")

    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        logging.info(f"Login successful for user: {user.first_name}")
        return jsonify({'token': token}), 200
    
    logging.warning(f"Invalid credentials for user: {data['first_name']}")
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear session data
    return jsonify({'message': 'Logged out successfully'}), 200
