import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

# TODO: make plot less ugly
class CategoryLifetime:

    @staticmethod
    def render(df):
        df = df[['category', 'date', 'first_observed', 'last_observed']] # only use relevant columns
        df['first_observed'] = pd.to_datetime(df['first_observed']) # turn dates into datetime objects
        df['last_observed'] = pd.to_datetime(df['last_observed'])
        df['product_lifetime'] = df['last_observed'] - df['first_observed']
        df['period'] = pd.DatetimeIndex(df['date']).to_period('Y')

        df_mean_ts = df.groupby(['period', 'category'])['product_lifetime'].mean(numeric_only=False)

        plot = df_mean_ts.unstack().plot.line()
        plot.plot()
        plt.show()

# CategoryLifetime.render(df)