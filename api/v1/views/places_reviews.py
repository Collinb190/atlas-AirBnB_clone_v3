#!/usr/bin/python3
"""flask app for users"""
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """get all review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """get a review objects"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False
)
def delete_review(review_id):
    """delete a review objects"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False
)
def create_review(place_id):
    """create review objects"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if "user_id" not in data.keys():
        abort(400, "Missing user_id")

    user = storage.get(User, data.get("user_id"))
    if not user:
        abort(404)
    if "text" not in data.keys():
        abort(400, "Missing text")

    data["place_id"] = place_id
    new_review = Review(**data)
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review object"""
    data = request.get_json(silent=True)
    review = storage.get(Review, review_id)
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    if not review:
        abort(404)
    elif not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
