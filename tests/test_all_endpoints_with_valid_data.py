import json
import unittest

from app import create_app, db
from global_vars import *

# print("hello", file=sys.stderr)


class TestAllEndpointsWithValidData(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # Binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_post_transaction_with_valid_data(self):
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "dark fruit",
                "value": 2.90,
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)
        result_data = str(res.data)
        self.assertIn("14 Nov 2013", result_data)  # date formatting issue
        self.assertIn("100.88", result_data)
        self.assertIn("Alcohol", result_data)
        self.assertIn("dark fruit", result_data)
        self.assertIn("2.9", result_data)  # Missing trailing zero, either string or client side

    def test_get_all_transactions_with_valid_data(self):
        transaction_one = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        transaction_two = json.dumps(
            {
                "date": "2019-01-31",
                "balance": 10.44,
                "category": "Food & juice",
                "description": "Weekly shop",
                "value": 23.50,
            }
        )

        res_one = self.client().post("/add_transaction", data=transaction_one, headers=HEADERS)
        self.assertEqual(res_one.status_code, 201)

        res_two = self.client().post("/add_transaction", data=transaction_two, headers=HEADERS)
        self.assertEqual(res_two.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("Weekly shop", result_data)

    def test_query_transactions_with_valid_data(self):
        transaction_one = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        transaction_two = json.dumps(
            {
                "date": "2019-01-31",
                "balance": 10.44,
                "category": "Food & juice",
                "description": "Weekly shop",
                "value": 23.50,
            }
        )

        res_one = self.client().post("/add_transaction", data=transaction_one, headers=HEADERS)
        self.assertEqual(res_one.status_code, 201)

        res_two = self.client().post("/add_transaction", data=transaction_two, headers=HEADERS)
        self.assertEqual(res_two.status_code, 201)

        res = self.client().get("/query_transactions?category=Alcohol")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("14 Nov 2013", result_data)
        self.assertIn("100.88", result_data)
        self.assertIn("Alcohol", result_data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("2.9", result_data)
        self.assertNotIn("31 Jan 2019", result_data)
        self.assertNotIn("10.44", result_data)
        self.assertNotIn("Food and Juice", result_data)
        self.assertNotIn("Weekly shop", result_data)
        self.assertNotIn("23.5", result_data)

    def test_delete_transactions_with_valid_data(self):
        transaction_one = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "Alcohol",
                "description": "Dark fruits",
                "value": 2.90,
            }
        )
        transaction_two = json.dumps(
            {
                "date": "2019-01-31",
                "balance": 10.44,
                "category": "Food & juice",
                "description": "Weekly shop",
                "value": 23.50,
            }
        )

        res_one = self.client().post("/add_transaction", data=transaction_one, headers=HEADERS)
        self.assertEqual(res_one.status_code, 201)

        res_two = self.client().post("/add_transaction", data=transaction_two, headers=HEADERS)
        self.assertEqual(res_two.status_code, 201)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertIn("Dark fruits", result_data)
        self.assertIn("Weekly shop", result_data)

        del_one = self.client().delete("/delete_transaction/1", headers=HEADERS)
        self.assertEqual(del_one.status_code, 200)

        res = self.client().get("/get_transactions")
        self.assertEqual(res.status_code, 200)
        result_data = str(res.data)
        self.assertNotIn("Dark fruits", result_data)
        self.assertIn("Weekly shop", result_data)

    def test_update_transaction_with_valid_data(self):
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
        self.assertEqual(res.status_code, 200)

        transactions = self.client().get("/get_transactions")
        self.assertEqual(transactions.status_code, 200)
        transactions_data = str(transactions.data)
        self.assertNotIn("14 Nov", transactions_data)
        self.assertIn("15 Nov", transactions_data)
        self.assertNotIn("Alcohol", transactions_data)
        self.assertIn("Other", transactions_data)
        self.assertNotIn("Dark fruits", transactions_data)
        self.assertIn("Strongbow dark fruits", transactions_data)
        self.assertNotIn("100.88", transactions_data)
        self.assertIn("13.33", transactions_data)
        self.assertNotIn("2.9", transactions_data)
        self.assertIn("3.9", transactions_data)

        # TODO - add in a check to make sure only one transaction exists here as unsure about
        # the affect of cached json here

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
