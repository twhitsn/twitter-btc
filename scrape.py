import json, calendar, csv, os.path
from datetime import date, timedelta, datetime

import pandas as pd

from twitterscraper import query_tweets
from twitterscraper.main import JSONEncoder

query = 'Bitcoin OR BTC'
poolsize = 20
limit = 1000 # number of posts per day

start_date = date(2017, 1, 1)

data_file = 'data.csv'

# check if data file already exists, if so we will continue from last retrieval
continued = os.path.isfile(data_file)

# get last date retrieved
if(continued):
    cur_data = pd.read_csv(data_file)
    last_date = cur_data.tail(1)['timestamp'].values[0].split('T')[0]
    start_date = datetime.strptime(last_date, '%Y-%m-%d').date() + timedelta(days = 1)
    
for m in range(start_date.month, 13):
    # number of days in current month
    monthend = calendar.monthrange(2017, m)[1]
    
    # use modified start date, or first of month
    days = range(start_date.day, monthend + 1) if m == start_date.month else range(1, monthend + 1)
    
    for d in days:
        print('Getting tweets for 2017-{}-{} ...'.format(m, d))
        
        cur_date = date(2017, m, d)

        # get tweets
        tweets = query_tweets(
            query, 
            poolsize = poolsize, 
            limit = limit * poolsize, 
            begindate = cur_date, 
            enddate = cur_date + timedelta(days = 1)
        )
        
        print('Retrieved', len(tweets), 'tweets.')
        
        tweets = [{k:v for k, v in json.loads(json.dumps(tweet, cls = JSONEncoder)).items() if k != 'html'} for tweet in tweets]
        
        print('Saving csv ...')
        if continued:
            old_df = pd.read_csv(data_file)
            all_df = pd.concat([old_df, pd.DataFrame(tweets)])
        else:
            all_df = pd.DataFrame(tweets)
            
        all_df.to_csv(data_file, index = False)
