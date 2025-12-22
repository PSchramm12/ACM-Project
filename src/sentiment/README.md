# Sentiment Analysis Module

This module provides sentiment analysis capabilities for social media text.

## Responsibilities (Pascal)

1. **Basic Sentiment Analysis**: Using VADER and TextBlob
2. **Sentiment Clustering**: Group tweets by sentiment patterns
3. **Topic-Based Sentiment**: Analyze sentiment for specific topics/policies (with Nicolai)

## Files

- `analyze_sentiment.py`: Main sentiment analysis script
- `clustering.py`: Sentiment clustering algorithms
- `topic_sentiment.py`: Topic-specific sentiment analysis

## Sentiment Analysis Methods

### VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Optimized for social media text
- Handles emojis, slang, and capitalization
- Returns compound score from -1 (most negative) to +1 (most positive)

### TextBlob
- Returns polarity (-1 to +1) and subjectivity (0 to 1)
- Good for general text sentiment

## Usage

### Basic Sentiment Analysis

```python
from src.sentiment.analyze_sentiment import SentimentAnalyzer

analyzer = SentimentAnalyzer()
df = analyzer.analyze_dataframe(df, text_column='text_clean')
```

### Topic-Based Sentiment Analysis

```python
from src.sentiment.analyze_sentiment import TopicSentimentAnalyzer

topic_analyzer = TopicSentimentAnalyzer()
df = topic_analyzer.analyze_topic_sentiment(df)

# Filter tweets about migration
migration_tweets = df[df['topic_migration'] == True]
```

## Output Columns

- `vader_pos`: Positive sentiment score (0-1)
- `vader_neg`: Negative sentiment score (0-1)
- `vader_neu`: Neutral sentiment score (0-1)
- `vader_compound`: Overall sentiment score (-1 to 1)
- `sentiment`: Classified sentiment ('positive', 'negative', 'neutral')
- `textblob_polarity`: TextBlob polarity score (-1 to 1)
- `textblob_subjectivity`: TextBlob subjectivity score (0 to 1)

## Topic Keywords

The topic keywords can be configured via the `config/topics.json` file. This allows you to easily add or modify topic definitions without changing code.

### Configuration Format

```json
{
  "topics": {
    "topic_name": {
      "keywords": ["keyword1", "keyword2"],
      "description": "Description of the topic"
    }
  }
}
```

### Currently Configured Topics

- **migration**: immigration, immigrant, border, migration, migrant, asylum
- **texas**: texas, tx
- **economy**: economy, economic, inflation, jobs, unemployment, gdp
- **healthcare**: healthcare, health care, obamacare, medicare, medicaid
- **climate**: climate, global warming, environment, clean energy, carbon
- **education**: education, school, university, college, student

### Custom Configuration

You can provide a custom configuration file:

```python
from src.sentiment.analyze_sentiment import TopicSentimentAnalyzer

# Use custom config
topic_analyzer = TopicSentimentAnalyzer(config_path='path/to/custom_topics.json')
```

If no config path is provided, the analyzer will look for `config/topics.json` in the project root, or fall back to default hardcoded keywords.
