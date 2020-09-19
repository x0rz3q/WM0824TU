import pandas as pd
import matplotlib.pyplot as plt

class VendorLifetime:
    @staticmethod
    def render(df, exclude=[]):
        df = df.drop(df[df['category'].isin(exclude)].index)
        df['period'] = pd.DatetimeIndex(df['date']).to_period('M')

        df_count_vendors = df.groupby(['period', 'category'])['vendor_hash'].count().unstack()

        plot = df_count_vendors.plot.line()
        plot.plot()
        plt.show()