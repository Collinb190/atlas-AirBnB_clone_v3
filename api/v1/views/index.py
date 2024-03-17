#!/usr/bin/python3
"""Script to start Flask app"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def api_status():
    """get status"""
    responce = {'status': "OK"}
    return jsonify(responce)
