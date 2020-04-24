#!/usr/bin/python3
"""Module for flask app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views, states


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db(Exception):
	"""remove SQLAlchemy session"""
	storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """Error handler for 404"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
	app.run('0.0.0.0', port=5000)
