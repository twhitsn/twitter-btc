# Twitter Sentiment and BTC Price

## Authors

- Tim Whitson @whitstd
- Debashish Dutta @deba21
- Santiago Garcia

## Usage

Run the scraping tool:

    python3 scrape.py
    
The tool will scrape Tweets by day (default 1000 per day). Each day is appended and saved to the csv file (default "data.csv"). Therefore, you can stop at any time and begin where you last left off.

**Use ctrl+z if exiting program while extracting. DO NOT use ctrl+c. If so, you will lose all progress.**