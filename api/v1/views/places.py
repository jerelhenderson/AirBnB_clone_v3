#!/usr/bin/python3
"""view for cities objs that handles default RESTful API actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models import storage


obj_dict = storage.all('Place')

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_place(city_id):
    """retrieves a list of Place objects given a place_id"""
    try:
        return jsonify([place.to_dict() for place in obj_dict.values()
                        if place.city_id == city_id])
    except:
        abort(404)

@app_views.route('/places/<place_id>', methods=['GET', 'DELETE'])
def get_place_obj(place_id):
    """gets Place obj based on id, else None if not found"""
    place_obj = storage.get('Place', place_id)
    if request.method == 'DELETE':
        if place_obj:
            place_obj.delete()
            storage.save()
        return jsonify({}), 200 if place_obj else abort(404)
    return jsonify(place_obj.to_dict()) if place_obj else abort(404)

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """creates a place"""
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    city_obj = storage.get('City', city_id)
    if not city_obj:
        abort(404)
    if 'user_id' not in content:
        return jsonify('Missing user_id'), 400
    user_obj = storage.get('User', city_id)
    if not user_obj:
        abort(404)
    if 'name' not in content:
        return jsonify('Missing name'), 400
    new_place = Place(**content)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/cities/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates a city obj"""
    place_obj = storage.get('Place', place_id)
    if not place_obj:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    for key, val in content.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(place_obj, key, val)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
