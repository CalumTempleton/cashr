import unittest
import sys

# Set the path of parent directory to import controller modules
sys.path.append('C:\\Users\\calum\\Documents\\CodePersonal\\cashr')
from flask_server_controller import app
from mysql_controller import *


# To run this test file: py flask_server_tests.py. Using unittest inside of pytest as
# it is a built in module
class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        db = connect_to_database()
        db.session.remove()
        db.drop_all()
        db.flush()
        db.rollback()  # these wont work as cant undo commit but need to do commit

    def test_index_page(self):
        response = self.app.get("/", content_type="html/text")

        self.assertEqual(response.data, b"Welcome to cashr")
        self.assertEqual(response.status_code, 200)

    def test_add_transaction_to_list(self):  # This is actually adding to my database. I shoudl create a test db
        response = self.app.post("/add_transactions",
                                 data='{"balance": 1.86, "date": "2011/11/11", "description": "limeee", "type": "food", "value": 3.33}',
                                 content_type="application/json")

        self.assertEqual(response.status_code, 4020)

    """
    def test_get_transactions(self):
        tester = app.test_client(self)
        response = tester.get("/get_transactions", content_type="application/json")

        self.assertEqual(response.data, b"Welcome to cashr")
        self.assertEqual(response.status_code, 200)
    """


if __name__ == "__main__":
    unittest.main()
