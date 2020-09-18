import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

# TODO: make plot less ugly
# TODO: deal with timeframes extending over multiple years
class CategoryLifetime:

    @staticmethod
    def render(df):
        df = df[['category', 'first_observed', 'last_observed']] # only use relevant columns
        df['first_observed'] = pd.to_datetime(df['first_observed']) # turn dates into datetime objects
        df['last_observed'] = pd.to_datetime(df['last_observed'])
        first_year = min(df['first_observed']).year
        last_year = max(df['last_observed']).year
        df['product_lifetime'] = df['last_observed'] - df['first_observed']

        dfs = []
        for i in range(first_year, last_year+1):
            df_by_year = df[(df['first_observed'] >= pd.Timestamp(str(i))) & (df['last_observed'] < pd.Timestamp(str(i+1)))]
            df_by_year_mean = df_by_year[['category', 'product_lifetime']].groupby('category').mean(numeric_only=False)
            df_by_year_mean['product_lifetime'] = df_by_year_mean['product_lifetime'].dt.days
            df_by_year_mean = df_by_year_mean.rename(columns={'product_lifetime': f'{str(i)}'})
            dfs.append(df_by_year_mean)

        df_mean_by_year = reduce(lambda df1,df2: pd.merge(df1,df2, on='category', how='outer'), dfs).transpose()
        plot = df_mean_by_year.plot.line()
        plot.plot()
        plt.show()
        
        return dfs

# dfs = CategoryLifetime.render(df)