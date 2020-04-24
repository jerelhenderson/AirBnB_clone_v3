#!/usr/bin/python3
"""view for places objs that handles default RESTful API actions"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.review import Review
from models import storage


obj_dict = storage.all('Review')

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_review(place_id):
    """retrieves a list of Review objects given a review_id"""
    try:
        return jsonify([review.to_dict() for review in obj_dict.values()
                        if review.place_id == place_id])
    except:
        abort(404)

@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE'])
def get_review_obj(review_id):
    """gets Review obj based on id, else None if not found"""
    review_obj = storage.get('Review', review_id)
    if request.method == 'DELETE':
        if review_obj:
            review_obj.delete()
            storage.save()
        return jsonify({}), 200 if review_obj else abort(404)
    return jsonify(review_obj.to_dict()) if review_obj else abort(404)

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """creates a review"""
    content = request.get_json()
    if not content:
        return jsonify('Not a JSON'), 400
    place_obj = storage.get('Place', place_id)
    if not place_obj:
        abort(404)
    if 'user_id' not in content:
        return jsonify('Missing user_id'), 400
    user_obj = storage.get('User', place_id)
    if not user_obj:
        abort(404)
    if 'text' not in content:
        return jsonify('Missing text'), 400
    new_review = Review(**content)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/places/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates a place obj"""
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
