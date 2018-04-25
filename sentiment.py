import re
import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords

for i in range(1, 4):
    print('Loading dataset {}...'.format(i))
    tweets = pd.read_csv('data/tweets{}.csv'.format(i))
    
    # remove rows where text is not a string
    tweets = tweets[tweets.text.apply(lambda t: type(t) is str)]
    
    # remove mentions, hashtags, and links
    tweets['text'] = tweets['text'].apply(lambda t: ' '.join(re.sub('(@[A-Za-z0-9]+)|[^ ]+\.[^ ]+', ' ', t).split()))
    
    # remove stop words
    print('Removing stop words and punctuation...')
    
    # cache stop words
    sw = stopwords.words('english')
    tweets['text'] = tweets['text'].apply(lambda t: ' '.join([word for word in t.split() if word not in sw]))
    
    # remove punctuation/non-ASCII characters
    tweets['text'] = tweets['text'].str.replace('[^\w\s]', '')

    print('Computing sentiment ...')
    
    polarity = []

    for j, tweet in enumerate(tweets['text']):
        print('{}%'.format(round(j / len(tweets) * 100)), end = '\r')    
        
        blob = TextBlob(tweet)
        polarity.append(blob.sentiment.polarity)
            
    sentiment = pd.DataFrame({'timestamp': tweets['timestamp'], 'polarity': polarity})
        
    print('Saving data/sentiment{}.csv'.format(i))
    sentiment.to_csv('data/sentiment{}.csv'.format(i), index = False)
