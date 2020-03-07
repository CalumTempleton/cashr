import json
import unittest

from app import create_app, db
from global_vars import *


class TestPostTransactionsWithInvalidData(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # Binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_delete_transaction_where_id_not_found(self):
        res = self.client().delete("/delete_transaction/2", headers=HEADERS)
        self.assertEqual(res.status_code, 404)
        self.assertIn("Cannot find transaction with ID of 2", res.data)

    def test_delete_transaction_where_id_a_string(self):
        res = self.client().delete("/delete_transaction/one", headers=HEADERS)
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
