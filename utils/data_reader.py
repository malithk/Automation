import csv
import os

def read_login_test_data():
    data = []
    file_path = os.path.join(os.path.dirname(__file__), "../test_data/login_credentials.csv")

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((row['username'], row['password'], row['expected_msg_part']))
    return data