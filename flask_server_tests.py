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

    def test_api_can_get_all_transactions(self):
        """Test API can get a transaction (GET request)."""
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
                "category": "Food and Juice",
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

    def test_post_transaction_with_invalid_date(self):
        """Test API handles a transaction with incorrect date format"""
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
        """Test API handles a transaction with an invalid category"""
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
        """Test API handles a transaction with an invalid description"""
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
