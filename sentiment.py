import pandas as pd
from textblob import TextBlob

tweets = pd.read_csv('data.csv')
tweets['Sentiment_Polarity'] = 'NA'

polarity = []

print('Computing sentiment ...')

for i, tweet in enumerate(tweets['text']):
    print('{}%'.format(round(i / len(tweets) * 100)), end = '\r')    
    
    if type(tweet) is str:
        blob = TextBlob(tweet)
        polarity.append(blob.sentiment.polarity)
        tweets.ix[i, 'Sentiment_Polarity'] = blob.sentiment.polarity
    else:
        polarity.append('')
    
tweets.to_csv('data_with_sentiment.csv')
print(polarity)
