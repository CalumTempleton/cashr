import json
import unittest

from app import create_app, db
from global_vars import *


class TestPostTransactionsWithInvalidData(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_post_transaction_with_invalid_date(self):
        transaction = json.dumps(
            {
                "date": "Thu, 14 Nov 2013",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "dark fruit",
                "value": 2.90,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)
        result_data = str(res.data)
        self.assertIn("date: True", result_data)
        self.assertIn("category: False", result_data)
        self.assertIn("description: False", result_data)
        self.assertIn("balance: False", result_data)
        self.assertIn("value: False", result_data)

        transaction = json.dumps(
            {
                "date": "01-01-2019",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "dark fruit",
                "value": 2.90,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)
        result_data = str(res.data)
        self.assertIn("date: True", result_data)
        self.assertIn("category: False", result_data)
        self.assertIn("description: False", result_data)
        self.assertIn("balance: False", result_data)
        self.assertIn("value: False", result_data)

    def test_post_transaction_with_invalid_category(self):
        transaction = json.dumps(
            {
                "date": "2019-01-01",
                "balance": 100.88,
                "category": "Invalid Category",
                "description": "dark fruit",
                "value": 2.90,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)
        result_data = str(res.data)
        self.assertIn("date: False", result_data)
        self.assertIn("category: True", result_data)
        self.assertIn("description: False", result_data)
        self.assertIn("balance: False", result_data)
        self.assertIn("value: False", result_data)

    def test_post_transaction_with_invalid_description(self):
        transaction = json.dumps(
            {
                "date": "2019-01-01",
                "balance": 100.88,
                "category": "Other",
                "description": "This is a really long description that will exceed the character limit. The character limited was added in to make sure the description does not exceed VARCHAR255 which is a good idea. Without this check, the database not accept the data, therefore causing the software to crash. Note the character limit has been set to 250 to be on the safe side.",
                "value": 2.90,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)
        result_data = str(res.data)
        self.assertIn("date: False", result_data)
        self.assertIn("category: False", result_data)
        self.assertIn("description: True", result_data)
        self.assertIn("balance: False", result_data)
        self.assertIn("value: False", result_data)

    def test_post_transaction_with_invalid_balance_and_values(self):
        """Test API handles a transaction with varying balance value. Note that it is difficult
        to make this test fail and that balance and value use the same verification function."""
        transaction = json.dumps(
            {
                "date": "2019-01-01",
                "balance": 0.8,
                "category": "Other",
                "description": "Tickets to Bermuda!",
                "value": 0.9,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)
        result_data = str(res.data)
        self.assertIn('"balance": 0.8', result_data)
        self.assertIn('"value": 0.9', result_data)

        transaction = json.dumps(
            {
                "date": "2019-01-01",
                "balance": 10001.11111111111,
                "category": "Other",
                "description": "Tickets to Bermuda!",
                "value": 122226.905,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)
        result_data = str(res.data)
        self.assertIn("date: False", result_data)
        self.assertIn("category: False", result_data)
        self.assertIn("description: False", result_data)
        self.assertIn("balance: True", result_data)
        self.assertIn("value: True", result_data)
        self.assertIn('"balance": 10001.11', result_data)
        self.assertIn('"value": 122226.9', result_data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
