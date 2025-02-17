#!/usr/bin/python3
"""The API endpoint for /api/v1/places/<place_id>/amenities"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity


@app_views.route(
    "/places/<place_id>/amenities",
    methods=["GET"],
    strict_slashes=False,
)
def get_amenities_by_place(place_id):
    """get amenities by place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage.__class__.__name__ == "DBStorage":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [
            storage.get(Amenity, amenity_id).to_dict()
            for amenity_id in place.amenity_ids
        ]
    return jsonify(amenities)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_amenity_from_place(place_id, amenity_id):
    """delete amenity from place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage.__class__.__name__ == "DBStorage":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def link_amenity_to_place(place_id, amenity_id):
    """link place to amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage.__class__.__name__ == "DBStorage":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
