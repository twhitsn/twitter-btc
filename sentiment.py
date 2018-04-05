import pandas as pd
from textblob import TextBlob

for i in range(1, 4):
    tweets = pd.read_csv('data/tweets{}.csv'.format(i))

    print('Computing sentiment for dataset {}...'.format(i))
    
    polarity = []

    for j, tweet in enumerate(tweets['text']):
        print('{}%'.format(round(j / len(tweets) * 100)), end = '\r')    
        
        if type(tweet) is str:
            blob = TextBlob(tweet)
            polarity.append(blob.sentiment.polarity)
        else:
            polarity.append('NA')
            
    sentiment = pd.DataFrame({'timestamp': tweets['timestamp'], 'polarity': polarity})
        
    print('Saving data/sentiment{}.csv'.format(i))
    sentiment.to_csv('data/sentiment{}.csv'.format(i), index = False)
