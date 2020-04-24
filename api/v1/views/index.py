#!/usr/bin/python3
"""df"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
	"""shows status"""
	return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=['GET'])
def stats():
	"""gets stats"""
	obj_dict = {'Amenity': 'amenities', 'City': 'cities', 'Place': 'places',
			    'Review': 'reviews', 'State': 'states', 'User': 'user'}
	return jsonify({val: storage.count(key) for key, val in obj_dict.items()})