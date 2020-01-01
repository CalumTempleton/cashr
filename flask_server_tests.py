import unittest
from app import create_app, db


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

    def test_transaction_creation(self):
        """Test API can create a transaction (POST request)"""
        transact = '{"date": "2013-11-14", "balance": 100.88, "category": "beer", "description": "dark fruit", "value": 2.90}'
        res = self.client().post('/add_transaction', data=transact)
        self.assertEqual(res.status_code, 201)
        self.assertIn('beer', str(res.data))

    def test_api_can_get_all_transactions(self):
        """Test API can get a transaction (GET request)."""
        transact = '{"date": "2013-11-14", "balance": 100.88, "category": "beer", "description": "dark fruit", "value": 2.90}'
        res = self.client().post('/add_transaction', data=transact)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/get_transactions')
        self.assertEqual(res.status_code, 200)
        self.assertIn('2.9', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()