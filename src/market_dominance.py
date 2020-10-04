import matplotlib.pyplot as plt
from qbstyles import mpl_style
import pandas as pd
from category_over_time import CategoryOverTime
import numpy as np

mpl_style(dark=False)

class MarketDominance:
    @staticmethod
    def render(df, split=True):
        for k,v in CategoryOverTime.mapping.items():
            df['category'] = df['category'].replace(k, v)
        
        # calculate the lifetime of the shop
        df['first_month'] = pd.DatetimeIndex(df['first_observed']).to_period('M')
        df['last_month'] = pd.DatetimeIndex(df['last_observed']).to_period('M')
        first_seen = df[['marketplace', 'first_month']].groupby(['marketplace']).min().unstack()['first_month']
        last_seen  = df[['marketplace', 'last_month']].groupby(['marketplace']).max().unstack()['last_month']

        df = df.groupby(['category', 'marketplace']).sum()['order_amount_usd'].unstack()
        df = df.fillna(0)

        # calculate the average per month for a given market
        for market in df:
            lifetime = (last_seen[market] - first_seen[market]).n
            df[market] = df[market] / lifetime

        if not split:
            ax = df.plot.bar(title='Category Revenue per Market', width=0.8, figsize=(10, 6))
            ax.set_xlabel('Category')
            ax.set_ylabel('Mean revenue per month in USD')
            ax.legend(title='Marketplace')
            ax.plot()
            plt.tight_layout()
            plt.savefig('market_dominance.pdf')
            plt.show()
        else:
            for market in df:
                ax = df[market].plot.bar(title=f'Category Revenue of {market}', width=0.8, figsize=(10, 6))
                ax.set_xlabel('Category')
                ax.set_ylabel('Average revenue per month in USD')
                ax.set_ylim(0, 200000)
                plt.yticks(np.arange(0, 200000+1, 50000))
                ax.plot()
                plt.tight_layout()
                plt.savefig(f"market_dominance-{market}.pdf")
                plt.clf()
                plt.figure()
                # plt.show()