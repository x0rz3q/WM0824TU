from argparse import ArgumentParser
import sqlite3
from os import path
import pandas as pd

def load_dataset(location):
    connection = sqlite3.connect(location)

    df = pd.read_sql_query("SELECT * FROM feedbacks left join items on feedbacks.item_hash = items.item_hash", connection)
    # remove duplicated columns
    df = df.loc[:, ~df.columns.duplicated()]
    # close connection
    connection.close()

    return df

if __name__ == '__main__':
    parser = ArgumentParser(description='Analyze the underground dataset')
    parser.add_argument('--dataset', required=True, type=str)

    args = parser.parse_args()
    location = args.dataset

    if not (path.exists(location) and path.isfile(location)):
        print("Please specify a valid path")
        exit(1)

    df = load_dataset(location)
    print(df.head())