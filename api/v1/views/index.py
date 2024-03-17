#!/usr/bin/python3
"""Script to start Flask app"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def api_status():
    """get status"""
    responce = {'status': "OK"}
    return jsonify(responce)


@app_views.route('/stats')
def get_stats():
    """get stats"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
