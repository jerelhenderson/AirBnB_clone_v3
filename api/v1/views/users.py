#!/usr/bin/python3
"""view for User objs that handles default RESTful API actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from models import storage


obj_dict = storage.all('User')

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_user():
    """retrieves a list of all User objects"""
    return jsonify([obj.to_dict() for obj in obj_dict.values()])

@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'])
def get_user_obj(user_id):
    """gets User obj based on id, else None if not found"""
    user_obj = storage.get('User', user_id)
    if request.method == 'DELETE':
        if user_obj:
            user_obj.delete()
            storage.save()
        return jsonify({}), 200 if user_obj else abort(404)
    return jsonify(user_obj.to_dict()) if user_obj else abort(404)

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """updates a user obj"""
    user_obj = storage.get('User', user_id)
    if not user_obj:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    for key, val in content.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(user_obj, key, val)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user"""
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    if 'email' not in content:
        return jsonify('Missing email'), 400
    if 'password' not in content:
        return jsonify('Missing password'), 400
    new_user = User(**content)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201
