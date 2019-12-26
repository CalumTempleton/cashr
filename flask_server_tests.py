# To run this test file: py.test flask_server_tests.py

import unittest

from flask_server_controller import app


class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type="html/text")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

"""
def test_example():
    name = "calum"
    assert name == "calm", "pass"
"""
