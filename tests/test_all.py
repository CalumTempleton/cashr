# python -m unittest tests/test_all.py

import unittest
import tests.test_endpoints as test_endpoints
import tests.test_endpoints_with_invalid_data as test_endpoints_with_invalid_data

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_endpoints))
suite.addTests(loader.loadTestsFromModule(test_endpoints_with_invalid_data))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
