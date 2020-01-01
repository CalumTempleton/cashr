import csv


def read_data_from_file():
    data_path = 'example_data.csv'
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        data = [r for r in reader]
        data.pop(0)  # Remove headers

    return data


def format_transactions(list_of_transactions):
    formatted_data = [[]]
    for transaction in list_of_transactions:
        # The format of the transaction is [balance, date, description, type, value]
        formatted_transaction = [transaction[4], transaction[0], transaction[2], "TBC", transaction[3]]
        formatted_data.append(formatted_transaction)
        print(formatted_transaction)

    return formatted_data


if __name__ == "__main__":
    transactions = read_data_from_file()
    formatted_transactions = format_transactions(transactions)
