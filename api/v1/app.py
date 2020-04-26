#!/usr/bin/python3
"""
Module: Flask
appy.py - handles Flask app related functions
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources="\*", origins='0.0.0.0')


@app.teardown_appcontext
def close_db(Exception):
    """ remove SQLAlchemy session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ handles errors for 404 """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(5000))
