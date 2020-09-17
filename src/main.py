from argparse import ArgumentParser
import sqlite3
from os import path
import pandas as pd

def load_dataset(location):
    connection = sqlite3.connect(location)

    feedback = pd.read_sql_query("SELECT * FROM feedbacks", connection)
    items = pd.read_sql_query("SELECT * FROM items", connection)

    connection.close()

    return (items, feedback)

if __name__ == '__main__':
    parser = ArgumentParser(description='Analyze the underground dataset')
    parser.add_argument('--dataset', required=True, type=str)

    args = parser.parse_args()
    location = args.dataset

    if not (path.exists(location) and path.isfile(location)):
        print("Please specify a valid path")
        exit(1)

    items, feedback = load_dataset(location)