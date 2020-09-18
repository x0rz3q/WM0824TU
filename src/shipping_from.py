import sqlite3

class ShippingFrom:
    @staticmethod
    def render(df):
        df = df.copy()

        # drop all non-countries
        to_drop = [
            'worldwide', ' worldwide', '', 'you', 'world.', 'web', 'internet', 'me on bmr', 'my email', 'torland', 'me', 'bmr', 'pm',
            'world', 'bm', 'foron', 'tor', 'the matrix', '------ worldwide', 'here', 'bmr pm', 'my inbox', 'ww', 'email', 'my bmr pm', 'my computer', 'inbox',
            'my', 'my pc', 'my pm', 'digital download', 'optiman', 'cyberspace', 'twilight zone', 'bettors paradise', 'international', 'bmr inbox', 'darknet',
            'undeclared', "atm's hack guides + biggest collection of ebooks/manuals", 'the united snakes of captivity', 'entire world', 'eu', 'europe',
            'centre europe', 'midwest usa', 'korea, north', 'my bmr', 'north korea', 'earth', 'asia', 'north america', 'eu in sealed envelope',
            'cherryflavor', 'www', 'browser', 'my bmr outbox', 'usa and canada', 'european union', '1 eucc no.1-- by pm', '5+5 eu cc by pm to', 'tor email',
            'tormail', 'cash out paypal--send with pm', 'a', 'bank', 'bm pm', 'direct dl', 'e-mail', 'computer', 'in pm', 'my tormail', 'somewhere', '*.*',
            'a                                                             b', 'europe or depots', 'n/a', 'online', 'us/uk', 'central europe', 'ftp site',
            'higher dimension', 'my hdd', 'net', 'netherlands / germany', 'travel agency', 'all', 'pmp,', '100+ carding site list--by pm', 'a boring central-eu country',
            'anywhere', 'b', 'biggest collection of ebooks/manuals store', 'european union (not from netherland)', 'iptorrents.com', 'my bmr account',
            'na', 'acecybersp', 'home', 'me pm', 'my download link', 'my hard drive', 'my@email', ''
        ]

        for value in to_drop:
            df.drop(df[df['ships_from'].str.lower() == value].index, inplace=True)

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
            'finland': 'Finland'
        }

        for k, v in mapping.items():
            df.replace(k, v, inplace=True)