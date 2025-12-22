"""
Unit tests for sentiment analysis module.

Run with: python -m pytest tests/
or install in development mode: pip install -e .
"""

import pytest
import pandas as pd

from src.sentiment.analyze_sentiment import SentimentAnalyzer, TopicSentimentAnalyzer


class TestSentimentAnalyzer:
    """Test cases for SentimentAnalyzer class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = SentimentAnalyzer()
    
    def test_classify_sentiment_positive(self):
        """Test positive sentiment classification."""
        result = self.analyzer.classify_sentiment(0.5)
        assert result == 'positive'
    
    def test_classify_sentiment_negative(self):
        """Test negative sentiment classification."""
        result = self.analyzer.classify_sentiment(-0.5)
        assert result == 'negative'
    
    def test_classify_sentiment_neutral(self):
        """Test neutral sentiment classification."""
        result = self.analyzer.classify_sentiment(0.0)
        assert result == 'neutral'


class TestTopicSentimentAnalyzer:
    """Test cases for TopicSentimentAnalyzer class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = TopicSentimentAnalyzer()
    
    def test_detect_topics_migration(self):
        """Test migration topic detection."""
        text = "The immigration policy at the border needs reform"
        topics = self.analyzer.detect_topics(text)
        assert 'migration' in topics
    
    def test_detect_topics_multiple(self):
        """Test multiple topic detection."""
        text = "Texas border policy affects the economy and immigration"
        topics = self.analyzer.detect_topics(text)
        assert 'migration' in topics
        assert 'texas' in topics
        assert 'economy' in topics
    
    def test_detect_topics_none(self):
        """Test no topics detected."""
        text = "Just a regular tweet about nothing specific"
        topics = self.analyzer.detect_topics(text)
        assert len(topics) == 0


if __name__ == '__main__':
    pytest.main([__file__])
