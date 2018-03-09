import pandas as pd

tweets = pd.read_csv('data_with_sentiment.csv')
tweets['date'], tweets['time'] = tweets['timestamp'].str.split('T', 1).str

BTC_price = pd.read_csv('bitcoin_market_price_2017.csv')
groups = tweets.groupby(['date']).mean().reset_index()

data_merged = pd.merge(BTC_price, groups, on="date")

columns = ['id', 'likes', 'replies', 'retweets']
data_merged.drop(columns, inplace=True, axis=1)
data_merged.rename(columns={'Sentiment_Polarity': 'Mean_Sentiment_Polarity'}, inplace=True)

#Placeholder - To add a new column to data_merge for correlation between price change and mean sentiment polarity.
#
data_merged.to_csv('bitcoin_market_price_2017.csv', index=False)
