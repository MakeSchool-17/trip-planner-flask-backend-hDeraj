from flask import Flask, request, make_response, jsonify, Response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from functools import wraps
import bcrypt

# Basic Setup
app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)


def bad(num):
    response = jsonify(data=[])
    response.status_code = num
    return response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    user_collection = app.db.users
    user = user_collection.find_one(
        {"username": username})

    if user is not None:
        hashed_pw = user['password']
        hashed = bcrypt.hashpw(password.encode("utf-8"),
                               hashed_pw.encode("utf-8")).decode("utf-8")
        return hashed_pw == hashed
    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# Implement REST Resource

class RegistrationResource(Resource):

    def post(self):
        new_user = request.json
        user_collection = app.db.users

        if 'password' not in new_user or 'username' not in new_user:
            return bad(403)

        user_exists = user_collection.find_one(
            {"username": new_user['username']})

        if user_exists is not None:
            return bad(403)

        hashed = bcrypt.hashpw(new_user['password'].encode("utf-8"),
                               bcrypt.gensalt(12)).decode("utf-8")
        user_collection.insert_one({"username": new_user['username'],
                                    "password": hashed})
        return user_collection.find_one(
            {"username": new_user['username']})

    @requires_auth
    def get(self):
        return "success"


class TripResource(Resource):
    @requires_auth
    def get(self, trip_id=None):
        trips_collection = app.db.trips
        if trip_id is None:
            return list(trips_collection.find({
                "username": request.authorization.username
            }))
        else:
            return list(trips_collection.find_one({
                "username": request.authorization.username,
                "trip_id": trip_id
            }))

    @requires_auth
    def post(self, trip_id=None):
        trips_collection = app.db.trips
        data = request.json

        if trip_id is None:
            if "trip_id" not in data:
                return bad(403)
        trip_id = trip_id if trip_id is not None else data['trip_id']

        trip_exists = trips_collection.find_one(
            {"username": request.authorization.username,
             "trip_id": trip_id})

        if trip_exists is not None:
            return bad(403)

        waypoints = [] if "waypoints" not in data else data["waypoints"]
        trip_name = "" if "trip_name" not in data else data["trip_name"]
        trip_date = "" if "trip_date" not in data else data["trip_date"]

        if trip_name == "" \
                or trip_date == "":
            return bad(403)

        trips_collection.insert_one({
            "waypoints": waypoints,
            "trip_name": trip_name,
            "trip_date": trip_date,
            "trip_id": trip_id,
            "username": request.authorization.username
        })

    @requires_auth
    def put(self, trip_id=None):
        pass


# Add REST resource to API
api.add_resource(RegistrationResource, '/register')
api.add_resource(TripResource, '/trips', '/trips/<trip_id>')


# provide a custom JSON serializer for flaks_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about
    # request related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
