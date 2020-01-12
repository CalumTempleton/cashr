import json
import unittest

from app import create_app, db

# print("hello", file=sys.stderr)

COLUMN_KEYS = ["date", "category", "description", "balance", "value"]
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


class TransactionsTestCase(unittest.TestCase):
    """This class represents the transaction test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_post_transaction_with_valid_data(self):
        """Test API can create a transaction (POST request)"""
        transaction = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "beer",
                "description": "dark fruit",
                "value": 2.90,
            }
        )

        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 201)
        result_as_string = str(res.data)
        self.assertIn("Thu, 14 Nov 2013", result_as_string)  # date formatting issue
        self.assertIn("100.88", result_as_string)
        self.assertIn("beer", result_as_string)
        self.assertIn("dark fruit", result_as_string)
        self.assertIn("2.9", result_as_string)  # float rounding issue with zero

    def test_api_can_get_all_transactions(self):
        """Test API can get a transaction (GET request)."""
        transaction_one = json.dumps(
            {
                "date": "2013-11-14",
                "balance": 100.88,
                "category": "beer",
                "description": "dark fruit",
                "value": 2.90,
            }
        )
        transaction_two = json.dumps(
            {
                "date": "2019-01-31",
                "balance": 10.44,
                "category": "food",
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
        result_as_string = str(res.data)
        self.assertIn("dark fruit", result_as_string)
        self.assertIn("Weekly shop", result_as_string)

    def test_post_transaction_with_invalid_date(self):
        """Test API handles a transaction with incorrect date format"""
        transaction = json.dumps(
            {
                "date": "Thu, 14 Nov 2013",
                "balance": 100.88,
                "category": "beer",
                "description": "dark fruit",
                "value": 2.90,
            }
        )
        res = self.client().post("/add_transaction", data=transaction, headers=HEADERS)
        self.assertEqual(res.status_code, 400)
        self.assertIn("beer", str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
