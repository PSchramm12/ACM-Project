# Data Preparation Module

This module handles the preparation and cleaning of social media data for sentiment analysis.

## Responsibilities (Pascal)

1. **Data Collection**: Scripts to collect Twitter/social media data
2. **Data Cleaning**: Remove duplicates, handle missing values, clean text
3. **Data Transformation**: Convert raw data into analysis-ready format
4. **Data Validation**: Ensure data quality and consistency

## Files

- `prepare_data.py`: Main script for data preparation
- `clean_text.py`: Text cleaning utilities
- `load_data.py`: Data loading functions
- `validate_data.py`: Data validation utilities

## Usage

### Basic Data Preparation

```python
from src.data_preparation.prepare_data import prepare_twitter_data

# Load and prepare data
df = prepare_twitter_data('data/raw/tweets.csv')
df.to_csv('data/processed/tweets_clean.csv', index=False)
```

### Text Cleaning

```python
from src.data_preparation.clean_text import clean_tweet_text

text = "RT @user: Check out this amazing #product! 🎉 https://example.com"
cleaned = clean_tweet_text(text)
# Output: "check out this amazing product"
```

## Data Format

### Input Format (Raw Data)
Expected CSV columns:
- `tweet_id`: Unique identifier
- `text`: Tweet text
- `created_at`: Timestamp
- `user_id`: User identifier
- `hashtags`: Hashtags used (optional)
- `retweet_count`: Number of retweets (optional)
- `favorite_count`: Number of favorites (optional)

### Output Format (Processed Data)
CSV columns:
- `tweet_id`: Unique identifier
- `text`: Original tweet text
- `text_clean`: Cleaned tweet text
- `created_at`: Timestamp (datetime format)
- `date`: Date only (for time series analysis)
- `user_id`: User identifier
- `hashtags`: List of hashtags
- `is_retweet`: Boolean flag
- `word_count`: Number of words in cleaned text
- `char_count`: Number of characters in cleaned text

## Data Quality Checks

1. Remove duplicate tweets
2. Remove tweets with missing text
3. Handle encoding issues
4. Validate timestamp format
5. Check for bot-like behavior patterns
