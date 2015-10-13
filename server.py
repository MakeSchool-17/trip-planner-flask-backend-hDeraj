from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.mongo_json_encoder import JSONEncoder

# Basic Setup
app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)


# Implement REST Resource
class TripObject(Resource):

    def post(self):
        new_trip_object = request.json
        trip_collection = app.db.trip_collection
        result = trip_collection.insert_one(new_trip_object)

        trip_object = trip_collection.find_one(
            {"_id": ObjectId(result.inserted_id)})

        return trip_object

    def get(self, trip_id):
        trip_collection = app.db.trip_collection
        trip_object = trip_collection.find_one({"_id": ObjectId(trip_id)})

        if trip_object is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return trip_object

# Add REST resource to API
api.add_resource(TripObject, '/trip/', '/trip/<string:trip_id>')


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
