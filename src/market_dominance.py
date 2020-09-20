import matplotlib.pyplot as plt
from qbstyles import mpl_style

mpl_style(dark=False)

class MarketDominance:
    @staticmethod
    def render(df, split=False):
        df = df.groupby(['category', 'marketplace']).sum()['order_amount_usd'].unstack()
        df = df.fillna(0)

        if not split:
            ax = df.plot.bar(title='Category Revenue per Market', width=0.8)
            ax.set_xlabel('Category')
            ax.set_ylabel('Revenue in USD')
            ax.legend(title='Marketplace')
            ax.plot()
            plt.tight_layout()
            plt.show()
        else:
            for market in df:
                ax = df[market].plot.bar(title=f'Category Revenue of {market}', width=0.8)
                ax.set_xlabel('Category')
                ax.set_ylabel('Revenue in USD')
                ax.plot()
                plt.tight_layout()
                plt.show()