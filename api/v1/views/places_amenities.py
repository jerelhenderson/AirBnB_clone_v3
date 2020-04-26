#!/usr/bin/python3
"""view for places objs that handles default RESTful API actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


obj_dict = storage.all('Amenity')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_place_amenity(place_id):
    """retrieves a list of Review objects given a review_id"""
    try:
        return jsonify([place_amenity.to_dict() for place_amenity in obj_dict.
                        values()
                        if place_amenity.place_id == place_id])
    except:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=
                 ['GET', 'DELETE'], strict_slashes=False)
def get_place_amenity_obj(place_id, amenity_id):
    """gets Place obj based on id, else None if not found"""
    place_obj = storage.get('Place', place_id)
    if request.method == 'DELETE':
        if place_obj:
            place_obj.delete()
            storage.save()
        return jsonify({}), 200 if place_obj else abort(404)
    return jsonify(place_obj.to_dict()) if place_obj else abort(404)

    amenity_obj = storage.get('Amenity', amenity_id)
    if request.method == 'DELETE':
        if amenity_obj:
            amenity_obj.delete()
            storage.save()
        return jsonify({}), 200 if amenity_obj else abort(404)
    return jsonify(amenity_obj.to_dict()) if amenity_obj else abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """creates a place_amenity"""
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    place_obj = storage.get('Place', place_id)
    if not place_obj:
        abort(404)
    amenity_obj = storage.get('Amenity', amenity_id)
    if not amenity_obj:
        abort(404)
    new_place_amenity = place_amenity(**content)
    new_place_amenity.amenity_id = amenity_id
    storage.new(new_place_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


""" @app_views.route('/places/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    \"""updates a place obj\"""
    review_obj = storage.get('Review', review_id)
    if not review_obj:
        abort(404)
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    for key, val in content.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(review_obj, key, val)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
"""
