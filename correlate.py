import pandas as pd

btc = pd.read_csv('data/bitcoin_market_price_2017.csv')
btc['date'] = pd.to_datetime(btc['date']).dt.date 

sentiment = pd.DataFrame()

print('Merging sentiment datasets ...')

# merge sentiment data
for i in range(1, 4):
    cur_sentiment = pd.read_csv('data/sentiment{}.csv'.format(i))
    cur_sentiment['date'] = pd.to_datetime(cur_sentiment['timestamp']).dt.date 
    sentiment = sentiment.append(cur_sentiment)    
    
print('Grouping sentiment dataset by day ...')

# get daily mean polarity
daily = sentiment.groupby('date', as_index = False)['polarity'].mean()
daily = daily.merge(btc, how = 'inner', on = 'date')

daily['polarity_diff'] = daily['polarity'].diff(1)
daily['polarity_bin'] = daily['polarity_diff'].apply(lambda x: 1 if x >= 0 else 0)
daily['change_bin'] = daily['change'].apply(lambda x: 1 if x >= 0 else 0)

# add lags
lags = 2

for i in range(1, lags + 1): 
    daily['polarity-{}'.format(i)] = daily['polarity'].shift(i).values

print('Computing correlation matrix ...') 
print(daily.corr())


