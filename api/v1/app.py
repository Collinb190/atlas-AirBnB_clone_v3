#!/usr/bin/python3
"""Script to start Flask app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Close the session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error"""
    responce = {"error": "Not found"}
    return jsonify(responce), 404


if __name__ == '__main__':
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(debug=True, host=HOST, port=PORT, threaded=True)
