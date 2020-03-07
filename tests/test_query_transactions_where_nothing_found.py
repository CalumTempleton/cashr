import json
import unittest

from app import create_app, db
from global_vars import *


class TestQueryTransactionsWhereNothingFound(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_query_transaction_where_date_not_found(self):
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

        res = self.client().get("/query_transactions?date=2019-02-18")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("2019-02-18", result_data)

    def test_query_transaction_where_category_not_found(self):
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

        res = self.client().get("/query_transactions?category=Flat")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Flat", result_data)

    def test_query_transaction_where_description_not_found(self):
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

        res = self.client().get("/query_transactions?description=stella")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("stella", result_data)

    def test_query_transaction_where_balance_and_values_not_found(self):
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

        res = self.client().get("/query_transactions?balance=100.87")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("100.87", result_data)

        res = self.client().get("/query_transactions?value=290.00")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("290.0", result_data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
