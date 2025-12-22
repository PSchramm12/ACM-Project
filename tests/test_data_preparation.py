"""
Unit tests for data preparation module.

Run with: python -m pytest tests/
or install in development mode: pip install -e .
"""

import pytest
import pandas as pd

from src.data_preparation.prepare_data import DataPreparator


class TestDataPreparator:
    """Test cases for DataPreparator class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.preparator = DataPreparator()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'tweet_id': [1, 2, 3, 4],
            'text': [
                'RT @user: This is a test tweet #hashtag https://example.com',
                'Another tweet without RT',
                'Duplicate tweet',
                'Duplicate tweet'
            ],
            'created_at': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-03']
        })
    
    def test_clean_text(self):
        """Test text cleaning function."""
        text = "RT @user: Check out this #amazing link https://example.com"
        cleaned = self.preparator.clean_text(text)
        
        assert '@user' not in cleaned
        assert 'https://example.com' not in cleaned
        assert 'RT' not in cleaned
        assert 'amazing' in cleaned  # hashtag symbol removed but word kept
    
    def test_clean_text_empty(self):
        """Test cleaning empty text."""
        cleaned = self.preparator.clean_text("")
        assert cleaned == ""
    
    def test_clean_text_none(self):
        """Test cleaning None value."""
        cleaned = self.preparator.clean_text(None)
        assert cleaned == ""
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        df = self.preparator.remove_duplicates(self.sample_data)
        assert len(df) == 3  # Should have 3 unique tweets
    
    def test_validate_data_valid(self):
        """Test validation with valid data."""
        result = self.preparator.validate_data(self.sample_data)
        assert result is True
    
    def test_validate_data_missing_columns(self):
        """Test validation with missing columns."""
        invalid_data = pd.DataFrame({'text': ['test']})
        with pytest.raises(ValueError):
            self.preparator.validate_data(invalid_data)
    
    def test_add_features(self):
        """Test feature addition."""
        df = self.sample_data.copy()
        df['text_clean'] = df['text'].apply(self.preparator.clean_text)
        df = self.preparator.add_features(df)
        
        assert 'word_count' in df.columns
        assert 'char_count' in df.columns
        assert 'is_retweet' in df.columns
        assert df.loc[0, 'is_retweet'] == True
        assert df.loc[1, 'is_retweet'] == False


if __name__ == '__main__':
    pytest.main([__file__])
