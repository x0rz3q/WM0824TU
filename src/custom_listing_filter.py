class CustomListingFilter:
    @staticmethod
    def filter(df):
        custom_listings = df[
            df.title.str.lower().str.contains('custom')
        ]

        item_hashes = custom_listings.groupby('item_hash').filter(lambda x: len(x) <= 1)[['item_hash']]

        return df[~df.item_hash.isin(item_hashes)]