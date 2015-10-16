import server
import unittest
import json
from pymongo import MongoClient
import base64


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        # Run app in testing mode to retrieve exceptions and stack traces
        server.app.config['TESTING'] = True

        # Inject test database into application
        mongo = MongoClient('localhost', 27017)
        db = mongo.test_database
        server.app.db = db

        # Drop collection (significantly faster than dropping entire db)
<<<<<<< HEAD
        db.drop_collection('trip_collection')
=======
        db.drop_collection('users')
        db.drop_collection('trips')
>>>>>>> development

    def test_registering_new_user(self):
        response = self.app.post(
<<<<<<< HEAD
            '/trip/',
            data=json.dumps(dict(name="A object")),
=======
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing"
                )),
>>>>>>> development
            content_type='application/json')

        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'user' in responseJSON["username"]

    def test_registering_existing_user(self):
        self.app.post(
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing2"
                )),
            content_type='application/json')

        response = self.app.post(
<<<<<<< HEAD
            '/trip/',
            data=json.dumps(dict(name="Another object")),
=======
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing"
                )),
>>>>>>> development
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        assert 'application/json' in response.content_type

<<<<<<< HEAD
        response = self.app.get('/trip/'+postedObjectID)
        responseJSON = json.loads(response.data.decode())
=======
    def test_unauthorized_trip_get(self):
        response = self.app.get(
            '/trips',
            content_type='application/json')
        self.assertEqual(response.status_code, 401)
        assert 'application/json' not in response.content_type

        response = self.app.get(
            '/trips',
            headers=[('Authorization', "Basic " +
                     base64.b64encode('user:testing2'.encode()).decode()),
                     ('Content-Type', 'application/json')])
        self.assertEqual(response.status_code, 401)
        assert 'application/json' not in response.content_type

    def test_authorized_trip_get(self):
        self.app.post(
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing2"
                )),
            content_type='application/json')

        response = self.app.get(
            '/trips',
            headers=[('Authorization', "Basic " +
                     base64.b64encode('user:testing2'.encode()).decode()),
                     ('Content-Type', 'application/json')])

        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type

    def test_unauthorized_trip_post(self):
        response = self.app.post(
            '/trips/1234',
            headers=[('Authorization', "Basic " +
                     base64.b64encode('user:testing2'.encode()).decode()),
                     ('Content-Type', 'application/json')])
        self.assertEqual(response.status_code, 401)
        assert 'application/json' not in response.content_type

    def test_authorized_trip_post(self):
        self.app.post(
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing2"
                )),
            content_type='application/json')

        response = self.app.post(
            '/trips/1234',
            data=json.dumps(dict(
                trip_name="test_trip",
                trip_date="june"
                )),
            headers=[('Authorization', "Basic " +
                     base64.b64encode('user:testing2'.encode()).decode()),
                     ('Content-Type', 'application/json')])

        self.assertEqual(response.status_code, 200)

        response = response = self.app.get(
            '/trips',
            headers=[('Authorization', "Basic " +
                     base64.b64encode('user:testing2'.encode()).decode()),
                     ('Content-Type', 'application/json')])
>>>>>>> development

        self.assertEqual(response.status_code, 200)
        trip = json.loads(response.data.decode())
        self.assertEqual(len(trip), 1)
        trip = trip[0]
        self.assertEqual(trip['trip_id'], "1234")
        self.assertEqual(trip['trip_name'], "test_trip")
        self.assertEqual(trip['trip_date'], "june")
        self.assertEqual(trip['waypoints'], [])
        self.assertEqual(trip['username'], "user")
        assert "_id" in trip

<<<<<<< HEAD
    def test_getting_non_existent_trip(self):
        response = self.app.get('/trip/55f0cbb4236f44b7f0e3cb23')
        self.assertEqual(response.status_code, 404)
=======
>>>>>>> development

if __name__ == '__main__':
    unittest.main()
