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

    @staticmethod
    def render_alt(df):
        # compute dfVendors
        vendorHashes, firstSeens, lastSeens = [], [], []
        for name, group in df.groupby('vendor_hash'):
            vendorHashes.append(name)
            firstSeens.append(min(group['first_observed'].min(), group['date'].min()))
            lastSeens.append(max(group['last_observed'].max(), group['date'].max()))
        dfVendors = pd.DataFrame(list(zip(vendorHashes, firstSeens, lastSeens)), columns =['vendor_hash', 'first_seen', 'last_seen']) 
        dfVendors['lifetime'] = dfVendors['last_seen'] - dfVendors['first_seen']
        dfVendors['lifetime'] = dfVendors['lifetime'].dt.days

        # compute dfMeanVendorLifetime
        periods = pd.date_range(start=pd.to_datetime('May 2011'), end=pd.to_datetime('May 2017'), freq='M').tolist()
        meanVendorLifetime = []
        for period in periods:
            meanVendorLifetime.append(dfVendors[(dfVendors['first_seen'] < period + pd.Timedelta(days=30)) & (dfVendors['last_seen'] > period)]['lifetime'].mean())
        
        # generate plot
        dfMeanVendorLifetime = pd.DataFrame(list(zip(periods, meanVendorLifetime)), columns =['month', 'mean_vendor_lifetime']) 
        ax = dfMeanVendorLifetime.plot.line(x='month', y='mean_vendor_lifetime', legend=False, title='Vendor lifetime over time')
        ax.set_xlabel("Time")
        ax.set_ylabel("Mean vendor lifetime (days)")
        ax.set_ylim(0, 750)
        ax.vlines(x=pd.to_datetime('October 2013'), ymin=0, ymax=750, linestyles='dashed', colors=['orange'])
        ax.text(pd.to_datetime('November 2013'), 200, 'SR1 take-down', rotation=90, va='center')
        ax.vlines(x=pd.to_datetime('November 6 2014'), ymin=0, ymax=750, linestyles='dashed', colors=['orange'])
        ax.text(pd.to_datetime('December 2014'), 200, 'Operation Onymous', rotation=90, va='center')
        ax.vlines(x=pd.to_datetime('August 2015'), ymin=0, ymax=750, linestyles='dashed', colors=['orange'])
        ax.text(pd.to_datetime('September 2015'), 200, 'Agora graceful exit', rotation=90, va='center')
        ax.plot()
        plt.show()