from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User, DeveloperProfile
from .. import db, limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"msg": "Email already exists"}), 400
    
    new_user = User(
        email=data.get('email'),
        full_name=data.get('full_name'),
        role=data.get('role', 'developer')
    )
    new_user.set_password(data.get('password'))
    
    db.session.add(new_user)
    db.session.flush() # To get the user ID
    
    if new_user.role == 'developer':
        profile = DeveloperProfile(user_id=new_user.id)
        db.session.add(profile)
        
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token, user_id=user.id, role=user.role), 200
    
    return jsonify({"msg": "Invalid email or password"}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "github_username": user.github_username
    }), 200
