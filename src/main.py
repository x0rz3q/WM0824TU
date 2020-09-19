from argparse import ArgumentParser
import sqlite3
from os import path
import pandas as pd
from filter import Filter

def load_dataset(location):
    connection = sqlite3.connect(location)

    df = pd.read_sql("SELECT * FROM feedbacks left join items on feedbacks.item_hash = items.item_hash", connection)
    # remove duplicated columns
    df = df.loc[:, ~df.columns.duplicated()]
    # convert bytestrings
    df['giver_hash'] = df['giver_hash'].str.decode("utf-8")
    df['receiver_hash'] = df['receiver_hash'].str.decode("utf-8")
    df['vendor_hash'] = df['vendor_hash'].str.decode("utf-8")
    # convert timestamps
    df['date'] = pd.to_datetime(df['date'])
    df['first_observed'] = pd.to_datetime(df['first_observed'])
    df['last_observed'] = pd.to_datetime(df['last_observed'])
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
    df = Filter.apply_all_filters(df)
