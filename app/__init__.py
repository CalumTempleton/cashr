import sys
from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Transactions

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
                'id': transaction.id,
                'date': transaction.date,
                'description': transaction.description,
                'category': transaction.category,
                'balance': transaction.balance,
                'value': transaction.value
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    # The curl command to test this endpoint is as follows: curl http://localhost:5000/query_transactions?description=pie
    @app.route("/query_transactions", methods=["GET"])
    def query_list_of_transaction():
        # This needs a null consideration and update by guide which has been faved on laptop
        description = request.args.get('description')  # This will need to be adapted for front end
        transactions = Transactions.query_by(description)
        results = []

        for transaction in transactions:
            obj = {
                'id': transaction.id,
                'date': transaction.date,
                'description': transaction.description,
                'category': transaction.category,
                'balance': transaction.balance,
                'value': transaction.value
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    # The curl command to test this endpoint is as follows:
    # curl -H "Content-Type: application/json" -X POST -d '{"date": "2017-06-15", "balance": 13.86, "category": "food", "description": "pie", "value": 3.33}' http://localhost:5000/add_transaction
    @app.route("/add_transaction", methods=["POST"])
    def add_transaction_to_list():
        req = request.get_data()
        my_json = req.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        date = data['date']
        category = data['category']
        description = data['description']
        balance = data['balance']
        value = data['value']
        if description:
            transaction = Transactions(date=date, description=description, category=category, balance=balance, value=value)
            transaction.save()
            response = jsonify({
                'id': transaction.id,
                'date': transaction.date,
                'description': transaction.description,
                'category': transaction.category,
                'balance': transaction.balance,
                'value': transaction.value
            })
            response.status_code = 201
            return response
        return 'An error has occurred'

    return app
