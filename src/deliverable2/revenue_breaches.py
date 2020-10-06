import pandas as pd
from scipy import stats
from seaborn import regplot
import matplotlib.pyplot as plt
import math


class RevenueBreaches:

    @staticmethod
    def render(df):
        breachesDataPath = "C:\\Users\\Linus\\OneDrive - student.tudelft.nl\\TUd\\Courses\\WM0824TU Economics of Cyber Security\\Project\\GitHub\\WM0824TU\\data\\data_breaches.csv"

        dfBreaches = pd.read_csv(breachesDataPath, sep="|", engine="python")

        # Preprocess breaches dataset
        dfBreaches = dfBreaches[['Entity', 'records lost', 'YEAR', 'story']]
        dfBreaches['date'] = dfBreaches['story'].astype(str).str[:9]
        dfBreaches['date'] = dfBreaches['date'].str.replace('.', '')
        dfBreaches = dfBreaches[dfBreaches['date'].str.contains(" 20")]
        dfBreaches['date'] = pd.to_datetime(dfBreaches['date'])
        dfBreaches['quartile'] = dfBreaches.apply(lambda x: "Q{} {}".format(math.ceil(x['date'].month / 3), x['date'].year), axis=1)

        # Compute number of breaches for each quartile
        breachesByQuartile = dfBreaches.groupby(['quartile']).size()
        breachesByQuartile = breachesByQuartile.rename("breaches")

        # Compute relative carding revenue per quartile
        df['quartile'] = df.apply(lambda x: "Q{} {}".format(math.ceil(x['date'].month / 3), x['date'].year), axis=1)
        revenueByQuartile = df[df['category']=='carding'].groupby(['quartile'])['order_amount_usd'].sum() / df.groupby(['quartile'])['order_amount_usd'].sum()
        revenueByQuartile = revenueByQuartile.rename("revenue")

        # Combine breaches and revenue
        dfBreachesRevenue = pd.concat([breachesByQuartile, revenueByQuartile], axis=1).dropna().reset_index()
        
        # Plot
        x = dfBreachesRevenue['revenue'].tolist()
        y = dfBreachesRevenue['breaches'].tolist()
        corr, p_value = stats.kendalltau(x, y)
        plt.figure(figsize=(7,5))
        ax = regplot(x=x, y=y, marker="+")
        ax.set(xlabel='Carding revenue share of total revenue per quartile', ylabel='Number of Major Breaches per quartile', title='Correlation Between Number of Data Breaches and Carding Revenue per Quartile')
        ax.text(max(x) * 0.8, max(y) * 0.95, r'$\tau$=' + str(round(corr, 2)) + '\np-value= ' + str(round(p_value, 2)))

        plt.show()