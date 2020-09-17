class Filter:
    @staticmethod
    def filter_custom_listings(df):
        custom_listings = df[
            df.title.str.lower().str.contains('custom')
        ]

        item_hashes = custom_listings.groupby('item_hash').filter(lambda x: len(x) <= 1)
        return df[~df.item_hash.isin(item_hashes['item_hash'])]

    @staticmethod
    def filter_drug_listings(dfItems):

        guide_keywords = ['book', 'guide', 'synthes', 'manufacture', 'homemade', 'bundle', 'how to', 'tutorial', 'manual']

        drug_keywords = [
            'alprazolam', 'hulk', 'percocet', 'pfizer', 'tavor', '0mg', '0 mg', '5mg', '5 mg', '0ug', '0 ug', 
            '5ug', '5 ug', 'µ', 'glue', 'preroll', 'pre-roll', 'ferrari', 'tesla', 'calvin klein', 'methyl', 
            'kush', 'amphetamine', 'mdma', '4fa', 'viagra', 'captagon', 'blotter', 'pill', 'microdot', '2c-', 
            'ambien', 'olam', 'epam', 'blunt', 'fentanyl', 'pvp', 'oxycodone', 'xanax', 'tablets', 'pillen', '250mg', 
            'hashman'
        ]

        df_guide_items = dfItems[dfItems['title'].str.lower().str.contains('|'.join(guide_keywords))]

        df_drug_related_items = dfItems[dfItems['title'].str.lower().str.contains('|'.join(drug_keywords))]
        df_drug_items = df_drug_related_items[~df_drug_related_items.index.isin(df_guide_items.index)]

        return dfItems[~dfItems.index.isin(df_drug_items.index)]

    @staticmethod
    def filter_misc(df):
        misc_keywords = ['tip jar', 'cyanid']

        df_misc_items = df[df['title'].str.lower().str.contains('|'.join(misc_keywords))]

        return df[~df.index.isin(df_misc_items.index)]

    @staticmethod
    def apply_all_filters(df):
        print(f"Size before filter: {df.shape[0]}")

        df = Filter.filter_custom_listings(df)
        print(f"Size after filtering custom listing: {df.shape[0]}")

        df = Filter.filter_drug_listings(df)
        print(f"Size after filtering drugs: {df.shape[0]}")

        df = Filter.filter_misc(df)
        print(f"Size after filtering misc: {df.shape[0]}")

        return df


