import server
import unittest
import json
from pymongo import MongoClient


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
        db.drop_collection('users')

    def test_registering_new_user(self):
        response = self.app.post(
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing"
                )),
            content_type='application/json')

        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'user' in responseJSON["username"]

    def test_posting_existing_user(self):
        self.app.post(
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing2"
                )),
            content_type='application/json')

        response = self.app.post(
            '/register',
            data=json.dumps(dict(
                username="user",
                password="testing"
                )),
            content_type='application/json')

        self.assertEqual(response.status_code, 403)
        assert 'application/json' in response.content_type

if __name__ == '__main__':
    unittest.main()
