import csv
import os

def load_csv_data(file_name):
    data_path = os.path.join("test_data", file_name)
    with open(data_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]