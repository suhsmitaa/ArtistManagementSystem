from flask import Blueprint, request, jsonify, current_app
from models.user import User
from routes.auth import token_required
from werkzeug.security import generate_password_hash



bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):
    if current_user.role != 'super_admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    page = request.args.get('page', 1, type=int)

    try:
        users = User.get_all(page=page)
        current_app.logger.debug(f"Fetched {len(users)} users for page {page}.")
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'message': 'Failed to fetch users', 'error': str(e)}), 500



@bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    if not all(key in data for key in ('first_name', 'last_name', 'email', 'password', 'role')):
        return jsonify({'message': 'Missing required fields'}), 400

   
    existing_user = User.get_by_first_name_and_email(data['first_name'], data['email'])

    if existing_user:
        return jsonify({'message': 'User with the same first name and email already exists'}), 400

  
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

        return jsonify({'message': 'User created successfully', 'user_id': new_user}), 201
    except Exception as e:
        current_app.logger.error(f"Error creating user: {str(e)}")
        return jsonify({'message': 'User creation failed', 'error': str(e)}), 400


    
@bp.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def user_operations(current_user, user_id):
    if current_user.role != 'super_admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify(user.to_dict()), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        
        user.phone = data.get('phone', user.phone)
        user.dob = data.get('dob', user.dob)
        user.gender = data.get('gender', user.gender)
        user.role = data.get('role', user.role)
        user.address = data.get('address', user.address)
        
        user.update()
        return jsonify({'message': 'User updated successfully'}), 200
    
    elif request.method == 'DELETE':
        User.delete(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
