#!/usr/bin/python3
'''Routes for the state object.
Routes:
    /cities: gets all the cities objects
    /cities/<city_id>: gets a specific city object matching the id
    /cities/<city_id>: deletes a specific city object matching id
    /cities/: posts a new city object
    /cities/<city_id>: updates a specific city object
'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<sd>/cities', methods=['GET'], strict_slashes=False)
def all_cities(sd):
    """Retrieves all the state objects"""
    states = storage.get("State", sd)
    if states is None:
        abort(404)

    lis = []
    for city in states.cities:
        lis.append(city.to_dict())
    return jsonify(lis)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    "Retrieves the state id from database else raises an error"
    states = storage.all("State")

    for state in states.values():
        for city in state.cities:
            if city.id == city_id:
                return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_id(city_id):
    """deletes a city object and returns an empty object\
            if found else raises a 404 error."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(sd):
    """Updates the database based on the city object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if not request.json:
        abort(404, "Not a JSON")

    ignore = ['id', 'created_at', 'state_id', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200


@app_views.route('/states/<s>/cities', methods=['POST'], strict_slashes=False)
def post_city(s):
    """Creates a new post"""
    if not request.json:
        abort(404, "Not a JSON")

    if 'name' not in request.json.keys():
        abort(404, "Missing name")

    city = City(**request.json)
    state = storage.get('State', s)
    if state is None:
        abort(404)

    city.state_id = state.id
    city.save()
    for cit in state.cities:
        return jsonify(cit.to_dict()), 201
