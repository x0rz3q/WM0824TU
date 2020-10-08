from argparse import ArgumentParser
from os import path
import pandas as pd
from filter import Filter
from main import load_dataset
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
from operator import attrgetter
from seaborn import regplot

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
    df['period'] = pd.DatetimeIndex(df['date']).to_period('M')

    df = df.groupby('vendor_hash').agg({
        'period': ['min', 'max'],
        'order_amount_usd': ['sum']
    })

    df.columns = ['period_min', 'period_max', 'sum']
    df = df.reset_index()
    df['period'] = (df['period_max'] - df['period_min']).apply(attrgetter('n'))
    df['period'] = df['period'].replace(0, 1)
    df['average'] = df['sum'] / df['period']

    # Remove outliers
    df = df[df['average'] < 20000]
    df = df[df['period'] < 50]

    df = df.fillna(0)

    x = df['period'].to_list()
    y = df['average'].to_list()

    corr, p_value = kendalltau(x,y)
    print(corr)

    plt.figure(figsize=(10,6))
    ax = regplot(x=x, y=y, marker="+")
    ax.set(xlabel='Period Active (Months)', ylabel='Average Monthly Sales (USD)', title='Correlation Between Vendor Lifetime and Average Monthly Sales')

    ax.text(40, max(y) - 2000, r'$\tau$=' + str(round(corr, 2)) + '\np-value= ' + str(round(p_value, 2)))
    
    plt.savefig('output.pdf')