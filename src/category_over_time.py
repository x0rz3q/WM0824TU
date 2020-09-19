import matplotlib.pyplot as plt
import pandas as pd
from qbstyles import mpl_style

mpl_style(dark=False)

class CategoryOverTime:
    @staticmethod
    def render(df):
        mapping = {
            'other - fake': 'fake',
            'other - guide': 'guide',
            'other - account': 'account',
            'other - custom': 'custom',
            'other - pirated software': 'pirated software',
            'other - voucher/invite/codes/lottery/gift': 'voucher/invite/codes/lottery/gift'
        }

        df['period'] = pd.DatetimeIndex(df['date']).to_period('M')

        for k,v in mapping.items():
            df['category'] = df['category'].replace(k, v)

        df = df.groupby(['period', 'category']).sum()['order_amount_usd'].unstack()
        df = df.fillna(0)

        ax = df.plot.line(title='Category Revenue over Time', style=['-'] * 10  + ['--'] * 10, linewidth=2)
        ax.set_xlabel('Month')
        ax.set_ylabel('Revenue in USD')
        ax.legend(title='Category')
        ax.plot()
        plt.show()