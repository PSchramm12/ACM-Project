"""
Sentiment Analysis Module

Provides sentiment analysis capabilities for social media text using multiple approaches:
- VADER (Valence Aware Dictionary and sEntiment Reasoner)
- TextBlob
- Topic-specific sentiment analysis

Author: Pascal
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Import sentiment analysis libraries
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    print("Warning: vaderSentiment not available. Install with: pip install vadersentiment")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("Warning: TextBlob not available. Install with: pip install textblob")


class SentimentAnalyzer:
    """Main class for sentiment analysis of social media text."""
    
    def __init__(self):
        """Initialize sentiment analyzers."""
        self.vader_analyzer = SentimentIntensityAnalyzer() if VADER_AVAILABLE else None
        
    def analyze_vader(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using VADER.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores (pos, neg, neu, compound)
        """
        if not self.vader_analyzer:
            return {'pos': 0, 'neg': 0, 'neu': 0, 'compound': 0}
        
        scores = self.vader_analyzer.polarity_scores(text)
        return scores
    
    def analyze_textblob(self, text: str) -> Tuple[float, float]:
        """
        Analyze sentiment using TextBlob.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (polarity, subjectivity)
        """
        if not TEXTBLOB_AVAILABLE:
            return (0.0, 0.0)
        
        blob = TextBlob(text)
        return (blob.sentiment.polarity, blob.sentiment.subjectivity)
    
    def classify_sentiment(self, compound_score: float) -> str:
        """
        Classify sentiment based on compound score.
        
        Args:
            compound_score: VADER compound score (-1 to 1)
            
        Returns:
            Sentiment label: 'positive', 'negative', or 'neutral'
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'text_clean') -> pd.DataFrame:
        """
        Perform sentiment analysis on a DataFrame of tweets.
        
        Args:
            df: DataFrame with tweets
            text_column: Name of column containing text to analyze
            
        Returns:
            DataFrame with added sentiment columns
        """
        print(f"Analyzing sentiment for {len(df)} tweets...")
        
        # VADER sentiment
        if VADER_AVAILABLE:
            print("Computing VADER sentiment scores...")
            vader_scores = df[text_column].apply(self.analyze_vader)
            df = pd.concat([
                df,
                pd.DataFrame(vader_scores.tolist(), index=df.index)
            ], axis=1)
            df['sentiment'] = df['compound'].apply(self.classify_sentiment)
            # Rename columns for clarity
            df.rename(columns={
                'pos': 'vader_pos',
                'neg': 'vader_neg',
                'neu': 'vader_neu',
                'compound': 'vader_compound'
            }, inplace=True)
        
        # TextBlob sentiment
        if TEXTBLOB_AVAILABLE:
            textblob_scores = df[text_column].apply(self.analyze_textblob)
            df['textblob_polarity'] = textblob_scores.apply(lambda x: x[0])
            df['textblob_subjectivity'] = textblob_scores.apply(lambda x: x[1])
        
        print("Sentiment analysis complete!")
        return df


class TopicSentimentAnalyzer:
    """Analyze sentiment directed at specific topics/policies."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize topic sentiment analyzer.
        
        Args:
            config_path: Path to topics configuration JSON file (optional)
        """
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # Load topic keywords from config or use defaults
        if config_path:
            self.topic_keywords = self._load_config(config_path)
        else:
            # Try to load from default location
            import os
            default_config = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'topics.json')
            if os.path.exists(default_config):
                self.topic_keywords = self._load_config(default_config)
            else:
                # Fallback to hardcoded defaults
                self.topic_keywords = {
                    'migration': ['immigration', 'immigrant', 'border', 'migration', 'migrant', 'asylum'],
                    'texas': ['texas', 'tx'],
                    'economy': ['economy', 'economic', 'inflation', 'jobs', 'unemployment', 'gdp'],
                    'healthcare': ['healthcare', 'health care', 'obamacare', 'medicare', 'medicaid'],
                    'climate': ['climate', 'global warming', 'environment', 'clean energy', 'carbon'],
                    'education': ['education', 'school', 'university', 'college', 'student'],
                }
    
    def _load_config(self, config_path: str) -> Dict[str, List[str]]:
        """Load topic keywords from JSON configuration file."""
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Extract just the keywords from the config structure
        return {topic: data['keywords'] for topic, data in config['topics'].items()}
    
    def detect_topics(self, text: str) -> List[str]:
        """
        Detect which topics are mentioned in the text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected topic names
        """
        text_lower = text.lower()
        detected = []
        
        for topic, keywords in self.topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(topic)
        
        return detected
    
    def analyze_topic_sentiment(self, df: pd.DataFrame, text_column: str = 'text_clean') -> pd.DataFrame:
        """
        Analyze sentiment for each topic.
        
        Args:
            df: DataFrame with tweets
            text_column: Name of column containing text
            
        Returns:
            DataFrame with topic detection and sentiment
        """
        print("Detecting topics in tweets...")
        df['topics'] = df[text_column].apply(self.detect_topics)
        df['has_topic'] = df['topics'].apply(lambda x: len(x) > 0)
        
        # Create binary columns for each topic
        for topic in self.topic_keywords.keys():
            df[f'topic_{topic}'] = df['topics'].apply(lambda x: topic in x)
        
        print(f"Topics detected: {df['has_topic'].sum()} tweets contain at least one topic")
        
        # Print topic distribution
        print("\nTopic Distribution:")
        for topic in self.topic_keywords.keys():
            count = df[f'topic_{topic}'].sum()
            print(f"  {topic}: {count} tweets")
        
        return df


def main():
    """Command-line interface for sentiment analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Perform sentiment analysis on Twitter data')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file path')
    parser.add_argument('--output', '-o', help='Output CSV file path')
    parser.add_argument('--topics', action='store_true', help='Include topic-based analysis')
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    df = pd.read_csv(args.input)
    
    # Perform sentiment analysis
    analyzer = SentimentAnalyzer()
    df = analyzer.analyze_dataframe(df)
    
    # Perform topic-based analysis if requested
    if args.topics:
        topic_analyzer = TopicSentimentAnalyzer()
        df = topic_analyzer.analyze_topic_sentiment(df)
    
    # Save results
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nResults saved to {args.output}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("Sentiment Analysis Summary")
    print("=" * 50)
    if 'sentiment' in df.columns:
        print("\nSentiment Distribution:")
        print(df['sentiment'].value_counts())
        print(f"\nAverage VADER Compound Score: {df['vader_compound'].mean():.3f}")


if __name__ == "__main__":
    main()
