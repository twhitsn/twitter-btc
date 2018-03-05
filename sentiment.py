import pandas as pd

tweets = pd.read_csv('data.csv')

print(tweets['text'])
