import csv


def read_data_from_file():
    data_path = 'example_data.csv'
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        data = [r for r in reader]
        data.pop(0)  # remove header

    return data


def format_data_from_file():
    formatted_data = [[]]
    for record in data:
        # The format of the record is [balance, date, description, type, value]
        formatted_record = [record[4], record[0], record[2], "TBC", record[3]]
        formatted_data.append(formatted_record)
        print(formatted_record)

    return formatted_data


if __name__ == "__main__":
    data = read_data_from_file()
    formatted_data = format_data_from_file()
