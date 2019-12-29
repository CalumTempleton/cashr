# import the Flask class from the flask module
from flask import Flask, jsonify, request
from mysql_controller import *

# create the application object
app = Flask(__name__)

"""
      "balance": 10.0, 
      "date": "Fri, 31 Jan 2020 00:00:00 GMT", 
      "description": "pints", 
      "type": "Banking", 
      "value": 5.0

transactionsl = [
    {
        "balance": 1,
        "date": "2020/01/31",
        "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
        "type": "Food shop",
        "value": 12.99,
    }
]
"""


# The curl command to test this endpoint is as follows: curl http://localhost:5000/get_transactions
@app.route("/get_transactions", methods=["GET"])
def get_list_of_transaction():
    transactions = get_transactions()
    return jsonify({"transactions": transactions})


# The curl command to test this endpoint is as follows:
# curl -i -H "Content-Type: application/json" -X POST -d '{"balance": 13.86, "date": "2020/01/31", "description": "pie", "type": "food", "value": 3.33}' http://localhost:5000/add_transactions
@app.route("/add_transactions", methods=["POST"])
def add_transaction_to_list():
    if not request.json or not "balance" in request.json:
        return "Not all data was included", 400
    else:
        balance = request.json["balance"]
        date = request.json["date"]
        description = request.json["description"]
        type = request.json["type"]
        value = request.json["value"]
        transaction = {
            "balance": balance,
            "date": date,
            "description": description,
            "type": type,
            "value": value,
        }
    add_transaction(balance, date, description, type, value)
    return jsonify({"transactions": transaction})


@app.route("/")
def index():
    return "Welcome to cashr"
