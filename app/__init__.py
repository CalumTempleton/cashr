import datetime
import sys

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from global_vars import CATEGORIES
from instance.config import app_config
from decimal import *

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Transactions

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.route("/")
    def index():
        return "Welcome to cashr"

    # The curl command to test this endpoint is as follows: curl http://localhost:5000/get_transactions
    @app.route("/get_transactions", methods=["GET"])
    def get_list_of_transaction():
        transactions = Transactions.get_all()
        results = []

        for transaction in transactions:
            obj = {
                "id": transaction.id,
                "date": transaction.date,
                "description": transaction.description,
                "category": transaction.category,
                "balance": float(transaction.balance),
                "value": float(transaction.value),
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    """
    The curl command to test this endpoint is as follows: 
    curl http://localhost:5000/query_transactions?description=pie
    """

    @app.route("/query_transactions", methods=["GET"])
    def query_list_of_transaction():
        # This needs a null consideration and update by guide which has been faved on laptop
        description = request.args.get("description")  # This will need to be adapted for front end
        transactions = Transactions.query_by(description)
        results = []

        for transaction in transactions:
            obj = {
                "id": transaction.id,
                "date": transaction.date,
                "description": transaction.description,
                "category": transaction.category,
                "balance": transaction.balance,
                "value": transaction.value,
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    """
    # The curl command to test this endpoint is as follows:
    curl -H "Content-Type: application/json" -X POST -d '{"date": "2017-06-15", "balance": 13.86, 
    "category": "Other", "description": "pie", "value": 3.33}' http://localhost:5000/add_transaction
    """

    @app.route("/add_transaction", methods=["POST"])
    def add_transaction_to_list():
        data = request.get_json(force=True)
        date, category, description, balance, value, error_list = get_json_values(data)

        if True not in error_list:
            transaction = Transactions(
                date=date, category=category, description=description, balance=balance, value=value
            )
            transaction.save()
            response = jsonify(
                {
                    "id": transaction.id,
                    "date": transaction.date,
                    "category": transaction.category,
                    "description": transaction.description,
                    "balance": float(transaction.balance),  # Decimals not serializable
                    "value": float(transaction.value),
                }
            )
            response.status_code = 201
            return response

        response = jsonify(
            {
                "error": "Invalid data entry! date: {}, category: {}, description: {}, balance: {}, value: {}".format(
                    error_list[0], error_list[1], error_list[2], error_list[3], error_list[4]
                ),
                "date": date,
                "category": category,
                "description": description,
                "balance": float(balance),
                "value": float(value),
            }
        )
        response.status_code = 400
        return response

    def get_json_values(
        data,
    ):  # move to helper class - also look at valid values for dates and floats
        keys = ["date", "category", "description", "balance", "value"]
        values = []
        for key in keys:
            if key not in data:
                # As category and balance are not required, this is only an issue for some keys.
                # This error handling will need to be improved
                values.append("null")
                raise ValueError("No key %s in JSON data!", key)
            else:
                values.append(data[key])

        date, date_error = verify_date(values[0])
        category, category_error = verify_category(values[1])
        description, description_error = verify_description(values[2])
        balance, balance_error = verify_monetary_values(values[3])
        value, value_error = verify_monetary_values(values[4])

        error_list = [date_error, category_error, description_error, balance_error, value_error]

        return date, category, description, balance, value, error_list

    def verify_date(date):
        error = False
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except:
            error = True
            make_error(400, "Error! Date out of range. Transactions from 2019 onward only.")

        return date, error

    def verify_category(category):
        error = False
        if category not in CATEGORIES:
            error = True
        return category, error

    def verify_description(description):
        error = False
        if len(description) >= 250:
            error = True
        return description, error

    # Note that there is no check for leading 0s as JSON does not handle this
    def verify_monetary_values(value):
        error = False
        try:
            value = Decimal(value)
            value = round(value, 2)
            if not isinstance(value, Decimal) or value > 10000.00:
                error = True
        except:
            error = True

        return value, error

    def make_error(status_code, message):
        response = jsonify({"status": status_code, "message": message})
        response.status_code = status_code
        return response

    return app
