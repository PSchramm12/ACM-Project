"""Test configuration and fixtures."""

import pytest
import pandas as pd


@pytest.fixture
def sample_tweet_data():
    """Sample tweet data for testing."""
    return pd.DataFrame({
        'tweet_id': [1, 2, 3],
        'text': [
            'I love this amazing policy! #great',
            'This is terrible and awful',
            'Just a normal neutral tweet'
        ],
        'created_at': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'user_id': ['user1', 'user2', 'user3']
    })


@pytest.fixture
def sample_polling_data():
    """Sample polling data for testing."""
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10),
        'poll_value': [45.0, 45.5, 46.0, 45.8, 45.2, 44.9, 45.3, 45.7, 46.1, 46.5]
    })
