#!/usr/bin/python3
"""
Module: Index
index.py - return JSON status for various objects
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ shows status of page """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ retrieves stats of objects """
    obj_dict = {'Amenity': 'amenities', 'City': 'cities', 'Place': 'places',
                'Review': 'reviews', 'State': 'states', 'User': 'users'}
    return jsonify({val: storage.count(key) for key, val in obj_dict.items()})
