import datetime
from decimal import *

from global_vars import CATEGORIES


def get_json_values(data):
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


def is_none(val):
    if val is None:
        return True
    else:
        return False


def get_id(data):
    if "id" in data:
        x = data["id"]
        return x
    else:
        return None


def verify_id(id):
    if is_none(id):
        return None, True
    else:
        return id, isinstance(id, int)


def verify_date(date):
    if is_none(date):
        return None, True
    else:
        error = False
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except:
            error = True
        return date, error


def verify_category(category):
    if is_none(category):
        return None, True
    else:
        error = False
        category = category.lower()
        category = category.capitalize()
        if category not in CATEGORIES:
            error = True
        return category, error


def verify_description(description):
    if is_none(description):
        return None, True
    else:  #
        error = False
        if len(description) >= 250:
            error = True
        return description, error


# Note that there is no check for leading 0s as JSON does not handle this
def verify_monetary_values(value):
    if is_none(value):
        return None, True
    else:
        error = False
        try:
            value = Decimal(value)
            value = round(value, 2)
            if not isinstance(value, Decimal) or value > 10000.00:
                error = True
        except:
            error = True

        return value, error
