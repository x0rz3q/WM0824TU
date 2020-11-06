import os
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num


class RedditRevenue:

    @staticmethod
    def render(df):
        dataDir = os.path.dirname(os.path.abspath(__file__)) + "/../../data/"
        dfGrowthDNM = pd.read_csv(dataDir + "darknetmarkets_growth.csv")
        dfGrowthDNMN = pd.read_csv(dataDir + "darknetmarketsnoobs_growth.csv")

        variants = [
            ("/r/DarkNetMarkets", "pre-February 2015"), 
            ("/r/DarkNetMarkets", "post-February 2015"), 
            ("/r/DarkNetMarketsNoobs", "pre-February 2015"), 
            ("/r/DarkNetMarketsNoobs", "post-February 2015")
            ]

        for (subreddit, period) in variants:
            if subreddit == "/r/DarkNetMarkets":
                dfRedditGrowth = dfGrowthDNM
            else:
                dfRedditGrowth = dfGrowthDNMN
            dfRedditGrowth['date'] = pd.to_datetime(dfRedditGrowth['date'])

            dfRevenue = df.groupby(['date'])['order_amount_usd'].sum().to_frame().reset_index()
            dfRevenue['date'] = pd.to_datetime(dfRevenue['date'])
            dfRevenue = dfRevenue.merge(dfRedditGrowth, on='date', how='inner')

            dfRevenue['growth'] = dfRevenue['growth'].rolling(7, center=True).mean()
            dfRevenue['order_amount_usd'] = dfRevenue['order_amount_usd'].rolling(7, center=True).mean()
            dfRevenue = dfRevenue.dropna()

            if period == "pre-February 2015":
                dfRevenue = dfRevenue[dfRevenue['date'] < pd.to_datetime('February 15 2015')]
            else:
                dfRevenue = dfRevenue[dfRevenue['date'] > pd.to_datetime('February 15 2015')]

            x = dfRevenue['order_amount_usd'].tolist()
            y = dfRevenue['growth'].tolist()
            corr, p_value = stats.kendalltau(x, y)

            from qbstyles import mpl_style
            mpl_style(dark=False)

            plt.figure(figsize=(10,6))
            points = plt.scatter(dfRevenue['order_amount_usd'], dfRevenue['growth'], c=[date2num(i.date()) for i in dfRevenue.date], s=20, cmap="plasma")
            plt.colorbar(points, format=DateFormatter('%b %y'))

            ax = sns.regplot("order_amount_usd", "growth", data=dfRevenue, scatter=False)

            #ax.set(xlabel='Daily Revenue in USD', ylabel='Daily Growth in Users', title='Subscriber Growth of {} vs. Revenue ({})'.format(subreddit, period))
            plt.ylim(bottom=-1)
            ax.text(max(x) * 0.8, max(y) * 0.95, r'$\tau$=' + str(round(corr, 2)) + '\np-value= ' + str(round(p_value, 2)))

            plt.show()