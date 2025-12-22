# Example Data Formats

This directory contains sample/example data files to illustrate the expected format for the project.

## Sample Tweet Data (`sample_tweets.csv`)

Example format for raw tweet data:

```csv
tweet_id,text,created_at,user_id,hashtags,retweet_count,favorite_count
1234567890,"Just voted today! #Election2024",2024-01-15 10:30:00,user123,"Election2024",5,12
1234567891,"RT @politician: Our new healthcare policy will help families",2024-01-15 11:45:00,user456,"",45,120
1234567892,"Gas prices are too high! We need change. #economy",2024-01-15 12:00:00,user789,"economy",2,8
```

## Sample Polling Data (`sample_polls.csv`)

Example format for polling data:

```csv
date,poll_value,poll_name,sample_size
2024-01-15,45.2,Approval Rating,1500
2024-01-16,45.5,Approval Rating,1500
2024-01-17,44.8,Approval Rating,1500
```

## Data Collection Instructions

### Twitter/X Data Collection

You can collect Twitter data using:

1. **Twitter API v2** (requires developer account):
```python
import tweepy

# Setup authentication
client = tweepy.Client(bearer_token="YOUR_BEARER_TOKEN")

# Search for tweets
tweets = client.search_recent_tweets(
    query="keyword -is:retweet",
    max_results=100,
    tweet_fields=['created_at', 'author_id', 'public_metrics']
)
```

2. **snscrape** (alternative, no API key needed):
```python
import snscrape.modules.twitter as sntwitter

# Search for tweets
tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper('keyword since:2024-01-01').get_items()):
    if i > 100:
        break
    tweets.append({
        'tweet_id': tweet.id,
        'text': tweet.content,
        'created_at': tweet.date,
        'user_id': tweet.user.id
    })
```

### Polling Data Sources

- RealClearPolitics
- FiveThirtyEight
- Gallup
- Pew Research Center

## Data Storage

- Raw data should be stored in `data/raw/`
- Processed data should be stored in `data/processed/`
- Both directories are excluded from git (see .gitignore)
- Always backup your data externally
