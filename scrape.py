import os
import platform
import json, calendar, csv, os.path, time
from datetime import date, timedelta, datetime
from random import randint
import pandas as pd
import twitterscraper.query
#from twitterscraper import query_tweets
from twitterscraper.main import JSONEncoder

# modify twitterscraper url
#   remove f=tweets, which sorts by newest
#   this will sort by top
twitterscraper.query.INIT_URL = "https://twitter.com/search?vertical=default&q={q}&l={lang}"
twitterscraper.query.RELOAD_URL = "https://twitter.com/i/search/timeline?vertical=" \
    "default&include_available_features=1&include_entities=1&" \
    "reset_error_state=false&src=typd&max_position={pos}&q={q}&l={lang}"

platform_type = platform.system()
query = 'bitcoin'
poolsize = 20
limit = 1000 # number of posts per day

start_date = date(2017, 9, 1)
end_month = 12

data_file = 'tweets3.csv'

sleep_time = 20 # seconds between requests

# check if data file already exists, if so we will continue from last retrieval
continued = os.path.isfile(data_file)

# get last date retrieved
if(continued):
    cur_data = pd.read_csv(data_file)
    last_date = cur_data.tail(1)['timestamp'].values[0].split('T')[0]
    start_date = datetime.strptime(last_date, '%Y-%m-%d').date() + timedelta(days = 1)
    
for m in range(start_date.month, end_month + 1):
    # number of days in current month
    monthend = calendar.monthrange(2017, m)[1]
    
    # use modified start date, or first of month
    days = range(start_date.day, monthend + 1) if m == start_date.month else range(1, monthend + 1)
    
    for d in days:
        print('Getting tweets for 2017-{}-{} ...'.format(m, d))
        
        cur_date = date(2017, m, d)

        # get tweets
        if platform_type == 'Linux':
            tweets = twitterscraper.query.query_tweets(
                query, 
                poolsize = poolsize, 
                limit = limit * poolsize, 
                begindate = cur_date, 
                enddate = cur_date + timedelta(days = 1),
                lang = 'en'
            )   
        elif platform_type == 'Windows':
            enddate = cur_date + timedelta(days = 1)
            command_str = 'twitterscraper "%s" --lang "en" -bd %s -ed %s -o temp_tweet.json -l %s'%(query, cur_date, enddate, limit)
            os.system('%s'%(command_str))
            with open('temp_tweet.json') as file:
                tweets = json.load(file)
            os.remove('temp_tweet.json')
        
        print('Retrieved', len(tweets), 'tweets.')
        
        tweets = [{k:v for k, v in json.loads(json.dumps(tweet, cls = JSONEncoder)).items() if k != 'html'} for tweet in tweets]
        
        print('Saving csv ...')
        if continued or cur_date > start_date:
            old_df = pd.read_csv(data_file)
            all_df = pd.concat([old_df, pd.DataFrame(tweets)])
        else:
            all_df = pd.DataFrame(tweets)
            
        all_df.to_csv(data_file, index = False)
        
        # sleep for random interval from 1-20 seconds
        time.sleep(randint(1, sleep_time))
