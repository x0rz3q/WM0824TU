import matplotlib.pyplot as plt
import pandas as pd

class CategoryOverTime:
    # TODO: Discuss this on Saturday, most likely needs to exclude some categories for it to become readable.
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

        plot = df.groupby(['period', 'category']).sum()['order_amount_usd'].unstack().plot.line()
        plot.plot()
        plt.show()