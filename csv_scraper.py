import csv
import numpy as np

if __name__ == "__main__":
    data_path = 'example_data.csv'
    with open(data_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # Skip headers as hardcoded and will never change
        data = []
        for row in reader:
            data.append(row)
            print(row)
