from argparse import ArgumentParser
from os import path
import pandas as pd
from filter import Filter
from main import load_dataset
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns

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

    to_drop = [
        'worldwide', ' worldwide', '', 'you', 'world.', 'web', 'internet', 'me on bmr', 'my email', 'torland', 'me', 'bmr', 'pm',
        'world', 'bm', 'foron', 'tor', 'the matrix', '------ worldwide', 'here', 'bmr pm', 'my inbox', 'ww', 'email', 'my bmr pm', 'my computer', 'inbox',
        'my', 'my pc', 'my pm', 'digital download', 'optiman', 'cyberspace', 'twilight zone', 'bettors paradise', 'international', 'bmr inbox', 'darknet',
        'undeclared', "atm's hack guides + biggest collection of ebooks/manuals", 'the united snakes of captivity', 'entire world', 'eu', 'europe',
        'centre europe', 'midwest usa', 'korea, north', 'my bmr', 'north korea', 'earth', 'asia', 'north america', 'eu in sealed envelope',
        'cherryflavor', 'www', 'browser', 'my bmr outbox', 'usa and canada', 'european union', '1 eucc no.1-- by pm', '5+5 eu cc by pm to', 'tor email',
        'tormail', 'cash out paypal--send with pm', 'a', 'bank', 'bm pm', 'direct dl', 'e-mail', 'computer', 'in pm', 'my tormail', 'somewhere', '*.*',
        'a                                                             b', 'europe or depots', 'n/a', 'online', 'us/uk', 'central europe', 'ftp site',
        'higher dimension', 'my hdd', 'net', 'netherlands / germany', 'travel agency', 'all', 'pmp,', '100+ carding site list--by pm', 'a boring central-eu country',
        'anywhere', 'b', 'biggest collection of ebooks/manuals store', 'european union (not from netherland)', 'iptorrents.com', 'my bmr account',
        'na', 'acecybersp', 'home', 'me pm', 'my download link', 'my hard drive', 'my@email', ''
    ]

    for value in to_drop:
        df.drop(df[df['ships_from'].str.lower() == value].index, inplace=True)

    # remap synonyms
    mapping = {
        'United States': 'United States of America',
        'United Stated Of America': 'United States of America',
        'The united States of America': 'United States of America',
        'USA': 'United States of America',
        'usa': 'United States of America',
        'us': 'United States of America',
        'Us': 'United States of America',
        'US': 'United States of America',
        'U.S.A': 'United States of America',
        'U.S.A.': 'United States of America',
        'Ships from: United States of America<br />': 'United States of America',
        'Holland': 'The Netherlands',
        'Netherlands': 'The Netherlands',
        'netherlands': 'The Netherlands',
        'singapore': 'Singapore',
        'nl': 'The Netherlands',
        'NL': 'The Netherlands',
        'the netherlands': 'The Netherlands',
        'fr': 'France',
        'FRANCE': 'France',
        'ger': 'Germany',
        'GER': 'Germany',
        'Germany (Monday and Thursday)': 'Germany',
        'GERMANY': 'Germany',
        'Germany (Monday and Friday)': 'Germany',
        'UK': 'United Kingdom',
        'Uk': 'United Kingdom',
        'UNITED KINGDOM': 'United Kingdom',
        'ITALY': 'Italy',
        'Hong Kong, (China)': 'Hong Kong',
        'france': 'France',
        'My@email or France': 'France',
        'Hong Kong SAR China': 'Hong Kong',
        'Russia (Russian Fed.)': 'Russia', 
        'AUSTRALIA': 'Australia',
        'finland': 'Finland'
    }

    for k, v in mapping.items():
        df.replace(k, v, inplace=True)

    gdp_df = pd.read_csv('data/gdp_per_capita.csv', sep=';')
    gdp_df['gdp'] = gdp_df[['2011', '2012', '2013', '2014', '2015', '2016', '2017']].mean(axis=1)
    pop_df = pd.read_csv('data/gdp_per_capita.csv', sep=';')

    gdp_df = gdp_df[['Country Name', 'gdp']]
    gdp_df['ships_from'] = gdp_df['Country Name']

    pop_df['pop'] = pop_df[['2011', '2012', '2013', '2014', '2015', '2016', '2017']].mean(axis=1)
    pop_df = pop_df[['Country Name', 'pop']]
    pop_df['ships_from'] = pop_df['Country Name']

    df = df.groupby('ships_from')['order_amount_usd'].sum()
    df = pd.merge(df, gdp_df, on='ships_from')
    df = pd.merge(df, pop_df, on='ships_from')
    
    df['order_amount_usd'] = df['order_amount_usd'] / df['pop']

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(1)

    # drop the outlier (Afghanistan)
    df = df.drop(df[df['order_amount_usd'] == df['order_amount_usd'].max()].index)

    y = df['order_amount_usd'].tolist()
    x = df['gdp'].tolist()

    corr, p_value = kendalltau(x, y)
    print(corr)
    print(p_value)

    plt.figure(figsize=(10,6))
    ax = sns.regplot(x=x, y=y, marker="+")
    ax.set(xlabel='GDP per Capita (USD)', ylabel='Sales per Capita (USD)', title='Correlation Between GDP per Capita and the Sales of Cybercrime per Capita')

    ax.text(140000, max(y) - 10, r'$\tau$=' + str(round(corr, 2)) + '\np-value= ' + str(round(p_value, 2)))
    
    plt.savefig('output.pdf')

    # plt.show()