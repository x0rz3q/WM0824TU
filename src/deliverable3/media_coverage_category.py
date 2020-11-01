from argparse import ArgumentParser
from os import path
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns
from qbstyles import mpl_style
from scipy.stats import kendalltau, zscore, shapiro

mpl_style(dark=False)

class MediaCoverageCategories:
    @staticmethod
    def render(df, next=False):
        mapping = {
            'other - fake': 'other',
            'other - guide': 'other',
            'other - account': 'other',
            'other - custom': 'other',
            'other - pirated software': 'other',
            'other - voucher/invite/codes/lottery/gift': 'other',
            'RAT': 'hacking services',
            'exploits': 'hacking services & tools',
            'botnet': 'hacking services & tools',
            'e-mail': 'hacking services & tools',
            'malware': 'hacking services & tools',
            'website': 'development',
            'app': 'development',
            'hosting': 'development',
            'carding': 'fraud',
            'phone': 'fraud'
        }

        for k,v in mapping.items():
            df['category'] = df['category'].replace(k, v)
        
        # Load in the black market media coverage dataset
        df_bm = pd.read_csv('../data/news_coverage.csv')[['date', 'count']]
        df_bm['date'] = pd.to_datetime(df_bm['date'])

        if next:
            df_bm['date'] = df_bm['date'] - pd.DateOffset(months=1)

        df_bm = df_bm.sort_values(by='date').reset_index(drop=True).dropna()
        df_bm['period'] = pd.DatetimeIndex(df_bm['date']).to_period('M')
        df_bm = df_bm.groupby('period').sum()

        dfBefore = df[df['date'] < pd.to_datetime('February 15 2015')]
        dfAfter = df[df['date'] > pd.to_datetime('February 15 2015')]

        titles = [
            'pre-February 2015',
            'post-February 2015'
        ]

        for (df, title) in zip([dfBefore, dfAfter], titles):
            # Calculate the periods
            df['period'] = pd.DatetimeIndex(df['date']).to_period('M')
            categories = df['category'].unique()

            df = df.groupby(['category', 'period'])['order_amount_usd'].sum()
            for category in categories:
                sub_set = pd.merge(df_bm, df[category], on='period')
                sub_set.fillna(0)

                x = sub_set['count'].tolist()
                y = sub_set['order_amount_usd'].tolist()
                
                corr, p_value = kendalltau(x, y)

                plt.figure(figsize=(10,6))
                ax = sns.regplot(x=x, y=y, marker="+")

                if next:
                    graph_title = f'Correlation Between Media Coverage of Black Markets of the Previous Month and Total Sales ({category}, {title})'
                else:
                    graph_title = f'Correlation Between Media Coverage of Black Markets and Total Sales ({category}, {title})'

                ax.set(xlabel='Monthly Media Coverage (# of Articles)', ylabel='Monthly Revenue in USD', title=graph_title)
                ax.text(max(x) * 0.8, max(y) * 0.95, r'$\tau$=' + str(round(corr, 2)) + '\np-value= ' + str(round(p_value, 2)))
                plt.savefig(f"figures/{category}-{title}.pdf")