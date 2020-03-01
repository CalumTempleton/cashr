import json
import unittest

from app import create_app, db
from global_vars import *


class TestQueryTransactionsWithInvalidData(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_query_transaction_with_invalid_date(self):
        transaction = json.dumps(
            {
                "date": "2019-02-28",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "dark fruit",
                "value": 2.90,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)

        res = self.client().get("/query_transactions?date=Today")
        self.assertEqual(res.status_code, 400)
        result_data = str(res.data)
        self.assertIn("Today", result_data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
