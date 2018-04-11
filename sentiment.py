import re #FIXME: delete???
import pandas as pd
from textblob import TextBlob

for i in range(1, 4):
    tweets = pd.read_csv('data/tweets{}.csv'.format(i))
    
    # remove rows where text is not a string
    tweets = tweets[tweets.text.apply(lambda t: type(t) is str)]
    
    # remove mentions and links
    tweets['text'] = tweets['text'].apply(lambda t: ' '.join(re.sub('(@[A-Za-z0-9]+)|[^ ]+\.[^ ]+', ' ', t).split()))
    
    # remove duplicate text
    tweets = tweets.drop_duplicates(['text'])

    print('Computing sentiment for dataset {}...'.format(i))
    
    polarity = []

    for j, tweet in enumerate(tweets['text']):
        print('{}%'.format(round(j / len(tweets) * 100)), end = '\r')    
        
        blob = TextBlob(tweet)
        polarity.append(blob.sentiment.polarity)
            
    sentiment = pd.DataFrame({'timestamp': tweets['timestamp'], 'polarity': polarity})
        
    print('Saving data/sentiment{}.csv'.format(i))
    sentiment.to_csv('data/sentiment{}.csv'.format(i), index = False)
