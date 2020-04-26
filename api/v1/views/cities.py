#!/usr/bin/python3
"""view for cities objs that handles default RESTful API actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models import storage


obj_dict = storage.all('City')


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_city(state_id):
    """retrieves a list of City objects given a city_id"""
    try:
        return jsonify([city.to_dict() for city in obj_dict.values()
                        if city.state_id == state_id])
    except:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_city_obj(city_id):
    """gets City obj based on id, else None if not found"""
    city_obj = storage.get('City', city_id)
    if request.method == 'DELETE':
        if city_obj:
            city_obj.delete()
            storage.save()
        return jsonify({}), 200 if city_obj else abort(404)
    return jsonify(city_obj.to_dict()) if city_obj else abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city"""
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    state_obj = storage.get('State', state_id)
    if not state_obj:
        abort(404)
    if 'name' not in content:
        return jsonify('Missing name'), 400
    new_city = City(**content)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a state obj"""
    city_obj = storage.get('City', city_id)
    if not city_obj:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    for key, val in content.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(city_obj, key, val)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
