"""Utility functions for the ACM project."""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any


def load_tweets(filepath: str) -> pd.DataFrame:
    """Load tweets from CSV file."""
    return pd.read_csv(filepath)


def save_tweets(df: pd.DataFrame, filepath: str) -> None:
    """Save tweets to CSV file."""
    df.to_csv(filepath, index=False)


def filter_by_date(df: pd.DataFrame, 
                  start_date: str, 
                  end_date: str, 
                  date_column: str = 'date') -> pd.DataFrame:
    """
    Filter DataFrame by date range.
    
    Args:
        df: DataFrame to filter
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        date_column: Name of date column
        
    Returns:
        Filtered DataFrame
    """
    df[date_column] = pd.to_datetime(df[date_column])
    mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
    return df[mask]


def filter_by_keywords(df: pd.DataFrame, 
                      keywords: List[str], 
                      text_column: str = 'text') -> pd.DataFrame:
    """
    Filter DataFrame to tweets containing any of the keywords.
    
    Args:
        df: DataFrame to filter
        keywords: List of keywords to search for
        text_column: Name of text column
        
    Returns:
        Filtered DataFrame
    """
    pattern = '|'.join(keywords)
    mask = df[text_column].str.contains(pattern, case=False, na=False)
    return df[mask]


def get_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get summary statistics for tweet DataFrame.
    
    Args:
        df: DataFrame with tweets
        
    Returns:
        Dictionary with summary statistics
    """
    stats = {
        'total_tweets': len(df),
        'unique_users': df['user_id'].nunique() if 'user_id' in df.columns else None,
        'date_range': (df['date'].min(), df['date'].max()) if 'date' in df.columns else None,
        'avg_word_count': df['word_count'].mean() if 'word_count' in df.columns else None,
    }
    
    if 'sentiment' in df.columns:
        stats['sentiment_distribution'] = df['sentiment'].value_counts().to_dict()
    
    return stats


def print_sample_tweets(df: pd.DataFrame, n: int = 5, sentiment: str = None) -> None:
    """
    Print sample tweets.
    
    Args:
        df: DataFrame with tweets
        n: Number of tweets to print
        sentiment: Filter by sentiment (optional)
    """
    if sentiment:
        sample = df[df['sentiment'] == sentiment].head(n)
    else:
        sample = df.head(n)
    
    for idx, row in sample.iterrows():
        print(f"\n--- Tweet {idx} ---")
        print(f"Text: {row['text'][:200]}...")
        if 'sentiment' in row:
            print(f"Sentiment: {row['sentiment']}")
        if 'vader_compound' in row:
            print(f"VADER Score: {row['vader_compound']:.3f}")
