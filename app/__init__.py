from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from app.endpoint_helper import *

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

    @app.route("/get_transactions", methods=["GET"])
    def get_list_of_transaction():
        """ The curl command to test this endpoint is as follows:
        curl http://localhost:5000/query_transactions
        """
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

    @app.route("/query_transactions", methods=["GET"])
    def query_list_of_transaction():
        """ The curl command to test this endpoint is as follows:
        curl http://localhost:5000/query_transactions?description=pie
        """
        # This needs a null consideration and update by guide which has been faved on laptop
        id = request.args.get("id")
        date = request.args.get("date")
        description = request.args.get("description")
        category = request.args.get("category")
        balance = request.args.get("balance")
        value = request.args.get("value")

        validation = {
            verify_id: [{"id": id}],
            verify_date: [{"date": date}],
            verify_category: [{"category": category}],
            verify_description: [{"description": description}],
            verify_monetary_values: [{"balance": balance}, {"value": value}],
        }

        filter_by_dict = {}
        c = ""

        for key, val in validation.items():
            for domain in val:
                for column, col_val in domain.items():
                    returned_val, error = key(col_val)
                    if returned_val is not None and error:  # The query column failed
                        response = jsonify(
                            {"Validation issue. The following query is not valid": returned_val}
                        )
                        response.status_code = 400
                        return response
                    elif not error:
                        filter_by_dict[column] = returned_val
                        c = column

        queried_transactions = Transactions.query_by(filter_by_dict)

        if len(queried_transactions) == 0:
            val = filter_by_dict[c]
            if isinstance(val, Decimal):
                response = jsonify(
                    {"Data issue. No transactions matching query for {} ".format(c): float(val)}
                )
            else:
                response = jsonify(
                    {"Data issue. No transactions matching query for {} ".format(c): val}
                )
            response.status_code = 200
            return response

        results = []
        for transaction in queried_transactions:
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

    @app.route("/add_transaction", methods=["POST"])
    def add_transaction_to_list():
        """ The curl command to test this endpoint is as follows: curl -H "Content-Type:
        application/json" -X POST -d '{"date": "2017-06-15", "balance": 13.86, "category":
        "Other", "description": "pie", "value": 3.33}' http://localhost:5000/add_transaction
        """
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

    return app
