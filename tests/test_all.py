# python -m unittest tests/test_all.py

import unittest
import tests.test_all_endpoints_with_valid_data as test_endpoints
import tests.test_post_transactions_with_invalid_data as test_post_transactions_with_invalid_data
import tests.test_query_transactions_with_invalid_data as test_query_transactions_with_invalid_data

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_endpoints))
suite.addTests(loader.loadTestsFromModule(test_post_transactions_with_invalid_data))
suite.addTests(loader.loadTestsFromModule(test_query_transactions_with_invalid_data))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
