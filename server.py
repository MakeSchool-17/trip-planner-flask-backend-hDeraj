from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
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


# Implement REST Resource
class UserResource(Resource):

    def post(self):
        new_user = request.json
        user_collection = app.db.users

        if 'password' not in new_user:
            return bad(403)

        user_exists = user_collection.find_one(
            {"username": new_user['username']})

        if not user_exists:
            hashed = bcrypt.hashpw(new_user['password'].encode("utf-8"),
                                   bcrypt.gensalt(12)).decode("utf-8")
            user_collection.insert_one({
                "username": new_user['username'],
                "password": hashed
            })
            return user_collection.find_one(
                {"username": new_user['username']})
        else:
            return bad(403)

# Add REST resource to API
api.add_resource(UserResource, '/users')


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
