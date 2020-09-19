import pandas as pd
import matplotlib.pyplot as plt

class ShippingTo:
    
    @staticmethod
    def filter_to_keep(df):
        countries_to_filter = df['ships_from'].unique().tolist()
        to_keep = set()
        df_countries = pd.read_csv('countries.csv').astype('str')
        for c1 in countries_to_filter:
            for c2 in df_countries.index:
                if df_countries.loc[c2]['Name'].lower() in c1.lower()\
                    or (len(c1.lower()) == 2 and c1.lower() in df_countries.loc[c2]['Code'].lower()):
                    to_keep.add(c1)
        return to_keep

    @staticmethod
    def render(df):
        to_keep = ShippingTo.filter_to_keep(df)

        df = df.drop(df[~df['ships_to'].isin(to_keep)].index, inplace=False)

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
            'finland': 'Finland',
            'PM': 'Saint Pierre and Miquelon'
        }

        for k, v in mapping.items():
            df.replace(k, v, inplace=True)

        df['period'] = pd.DatetimeIndex(df['date']).to_period('M')
        to_display = df.groupby('ships_to')['order_amount_usd'].count().nlargest(8).index.tolist()
        df = df[df['ships_to'].isin(to_display)]
        df = df.groupby(['period', 'ships_to']).count()['order_amount_usd'].unstack()
        df = df.fillna(0)

        ax = plot = df.plot.line(title='Import of Cybercrime per Country in a Monthly Period')
        ax.set_xlabel('Month')
        ax.set_ylabel('Export')
        ax.legend(title='Country')
        plot.plot()
        plt.show()

        return df

# df1 = ShippingTo.render(df)