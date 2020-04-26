#!/usr/bin/python3
"""view for Amenity objs that handles default RESTful API actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


obj_dict = storage.all('Amenity')


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenity():
    """retrieves a list of all Amenity objects"""
    return jsonify([obj.to_dict() for obj in obj_dict.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_amenity_obj(amenity_id):
    """gets Amenity obj based on id, else None if not found"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if request.method == 'DELETE':
        if amenity_obj:
            amenity_obj.delete()
            storage.save()
        return jsonify({}), 200 if amenity_obj else abort(404)
    return jsonify(amenity_obj.to_dict()) if amenity_obj else abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a amenity"""
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    if 'name' not in content:
        return jsonify('Missing name'), 400
    new_amenity = Amenity(**content)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates a amenity obj"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if not amenity_obj:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    for key, val in content.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(amenity_obj, key, val)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
