import pandas as pd
from textblob import TextBlob

tweets = pd.read_csv('data.csv')

polarity = []

print('Computing sentiment ...')

for i, tweet in enumerate(tweets['text']):
    print('{}%'.format(round(i / len(tweets) * 100)), end = '\r')    
    
    if type(tweet) is str:
        blob = TextBlob(tweet)
        polarity.append(blob.sentiment.polarity)
    else:
        polarity.append('')
    
print(polarity)
