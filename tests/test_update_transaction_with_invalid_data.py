import json
import unittest

from app import create_app, db
from global_vars import *


class TestUpdateTransactionsWithInvalidData(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_update_transaction_with_invalid_date(self):
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        updated_transaction = json.dumps(
            {
                "date": "Today",
                "balance": 13.33,
                "category": "Other",
                "description": "Strongbow dark fruits",
                "value": 3.90,
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("1", result_data)  # id

        res = self.client().put("/update_transaction/1", data=updated_transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)

        transactions = self.client().get("/get_transactions")
        self.assertEqual(transactions.status_code, 200)
        transactions_data = str(transactions.data)
        self.assertIn("14 Nov", transactions_data)
        self.assertNotIn("Today", transactions_data)
        self.assertIn("Alcohol", transactions_data)
        self.assertNotIn("Other", transactions_data)
        self.assertIn("Dark fruits", transactions_data)
        self.assertNotIn("Strongbow dark fruits", transactions_data)
        self.assertIn("100.88", transactions_data)
        self.assertNotIn("13.33", transactions_data)
        self.assertIn("2.9", transactions_data)
        self.assertNotIn("3.9", transactions_data)

    def test_update_transaction_with_invalid_category(self):
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        updated_transaction = json.dumps(
            {
                "date": "2013-11-15",
                "balance": 13.33,
                "category": "Soda Pop",
                "description": "Strongbow dark fruits",
                "value": 3.90,
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("1", result_data)  # id

        res = self.client().put("/update_transaction/1", data=updated_transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)

        transactions = self.client().get("/get_transactions")
        self.assertEqual(transactions.status_code, 200)
        transactions_data = str(transactions.data)
        self.assertIn("14 Nov", transactions_data)
        self.assertNotIn("15 Nov", transactions_data)
        self.assertIn("Alcohol", transactions_data)
        self.assertNotIn("Soda Pop", transactions_data)
        self.assertIn("Dark fruits", transactions_data)
        self.assertNotIn("Strongbow dark fruits", transactions_data)
        self.assertIn("100.88", transactions_data)
        self.assertNotIn("13.33", transactions_data)
        self.assertIn("2.9", transactions_data)
        self.assertNotIn("3.9", transactions_data)

    def test_update_transaction_with_invalid_description(self):
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        updated_transaction = json.dumps(
            {
                "date": "2013-11-15",
                "balance": 13.33,
                "category": "Other",
                "description": LONG_DESCRIPTION,
                "value": 3.90,
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("1", result_data)  # id

        res = self.client().put("/update_transaction/1", data=updated_transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)

        transactions = self.client().get("/get_transactions")
        self.assertEqual(transactions.status_code, 200)
        transactions_data = str(transactions.data)
        self.assertIn("14 Nov", transactions_data)
        self.assertNotIn("15 Nov", transactions_data)
        self.assertIn("Alcohol", transactions_data)
        self.assertNotIn("Other", transactions_data)
        self.assertIn("Dark fruits", transactions_data)
        self.assertNotIn(LONG_DESCRIPTION, transactions_data)
        self.assertIn("100.88", transactions_data)
        self.assertNotIn("13.33", transactions_data)
        self.assertIn("2.9", transactions_data)
        self.assertNotIn("3.9", transactions_data)

    def test_update_transaction_with_invalid_balance(self):
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        updated_transaction = json.dumps(
            {
                "date": "2013-11-15",
                "balance": "100.00.1",
                "category": "Other",
                "description": "Soda Pop",
                "value": 3.90,
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("1", result_data)  # id

        res = self.client().put("/update_transaction/1", data=updated_transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)

        transactions = self.client().get("/get_transactions")
        self.assertEqual(transactions.status_code, 200)
        transactions_data = str(transactions.data)
        self.assertIn("14 Nov", transactions_data)
        self.assertNotIn("15 Nov", transactions_data)
        self.assertIn("Alcohol", transactions_data)
        self.assertNotIn("Other", transactions_data)
        self.assertIn("Dark fruits", transactions_data)
        self.assertNotIn("Soda Pop", transactions_data)
        self.assertIn("100.88", transactions_data)
        self.assertNotIn("100.00.1", transactions_data)
        self.assertIn("2.9", transactions_data)
        self.assertNotIn("3.9", transactions_data)

    def test_update_transaction_with_invalid_value(self):
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        updated_transaction = json.dumps(
            {
                "date": "2013-11-15",
                "balance": 100.99,
                "category": "Other",
                "description": "Soda Pop",
                "value": "One Hundred",
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("1", result_data)  # id

        res = self.client().put("/update_transaction/1", data=updated_transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)

        transactions = self.client().get("/get_transactions")
        self.assertEqual(transactions.status_code, 200)
        transactions_data = str(transactions.data)
        self.assertIn("14 Nov", transactions_data)
        self.assertNotIn("15 Nov", transactions_data)
        self.assertIn("Alcohol", transactions_data)
        self.assertNotIn("Other", transactions_data)
        self.assertIn("Dark fruits", transactions_data)
        self.assertNotIn("Soda Pop", transactions_data)
        self.assertIn("100.88", transactions_data)
        self.assertNotIn("100.99", transactions_data)
        self.assertIn("2.9", transactions_data)
        self.assertNotIn("One Hundred", transactions_data)

    def test_update_transaction_with_no_change(self):
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        updated_transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("1", result_data)  # id

        res = self.client().put("/update_transaction/1", data=updated_transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 200)

        transactions = self.client().get("/get_transactions")
        self.assertEqual(transactions.status_code, 200)
        transactions_data = str(transactions.data)
        # self.assertIn("Request valid but transaction not updated due to no change in data", transactions_data)
        self.assertIn("14 Nov", transactions_data)
        self.assertIn("Alcohol", transactions_data)
        self.assertIn("Dark fruits", transactions_data)
        self.assertIn("100.88", transactions_data)
        self.assertIn("2.9", transactions_data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
