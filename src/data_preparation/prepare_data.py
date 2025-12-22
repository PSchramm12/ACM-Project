"""
Data Preparation Module

Main script for preparing Twitter/social media data for sentiment analysis.
Handles data loading, cleaning, and transformation.

Author: Pascal
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import Optional, List
import warnings
warnings.filterwarnings('ignore')


class DataPreparator:
    """Main class for data preparation tasks."""
    
    def __init__(self):
        self.required_columns = ['tweet_id', 'text', 'created_at']
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load raw tweet data from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with raw tweet data
        """
        try:
            df = pd.read_csv(filepath)
            print(f"Loaded {len(df)} rows from {filepath}")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate that required columns exist.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        return True
    
    def clean_text(self, text: Optional[str]) -> str:
        """
        Clean tweet text by removing URLs, mentions, special characters.
        
        Args:
            text: Raw tweet text (can be None)
            
        Returns:
            Cleaned text
        """
        if pd.isna(text) or text is None:
            return ""
        
        # Convert to string
        text = str(text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        
        # Remove RT indicator
        text = re.sub(r'^RT\s+', '', text)
        
        # Remove hashtag symbol but keep the word
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Convert to lowercase
        text = text.lower()
        
        return text.strip()
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate tweets based on text content.
        
        Args:
            df: DataFrame with tweets
            
        Returns:
            DataFrame without duplicates
        """
        initial_count = len(df)
        df = df.drop_duplicates(subset=['text'], keep='first')
        removed = initial_count - len(df)
        print(f"Removed {removed} duplicate tweets")
        return df
    
    def parse_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse and standardize datetime column.
        
        Args:
            df: DataFrame with created_at column
            
        Returns:
            DataFrame with parsed datetime
        """
        try:
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['date'] = df['created_at'].dt.date
            print("Successfully parsed datetime column")
        except Exception as e:
            print(f"Warning: Could not parse datetime column: {e}")
        return df
    
    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add additional features for analysis.
        
        Args:
            df: DataFrame with cleaned tweets
            
        Returns:
            DataFrame with additional features
        """
        # Add word count
        df['word_count'] = df['text_clean'].apply(lambda x: len(str(x).split()))
        
        # Add character count
        df['char_count'] = df['text_clean'].apply(lambda x: len(str(x)))
        
        # Check if retweet
        df['is_retweet'] = df['text'].str.startswith('RT ')
        
        return df
    
    def prepare_data(self, 
                    input_path: str, 
                    output_path: Optional[str] = None) -> pd.DataFrame:
        """
        Main pipeline for data preparation.
        
        Args:
            input_path: Path to raw data CSV
            output_path: Path to save processed data (optional)
            
        Returns:
            Processed DataFrame
        """
        print("=" * 50)
        print("Starting Data Preparation Pipeline")
        print("=" * 50)
        
        # Load data
        df = self.load_data(input_path)
        
        # Validate data
        self.validate_data(df)
        
        # Remove duplicates
        df = self.remove_duplicates(df)
        
        # Remove rows with missing text
        initial_count = len(df)
        df = df.dropna(subset=['text'])
        removed = initial_count - len(df)
        print(f"Removed {removed} rows with missing text")
        
        # Clean text
        print("Cleaning text...")
        df['text_clean'] = df['text'].apply(self.clean_text)
        
        # Remove empty cleaned texts
        initial_count = len(df)
        df = df[df['text_clean'].str.len() > 0]
        removed = initial_count - len(df)
        print(f"Removed {removed} rows with empty cleaned text")
        
        # Parse datetime
        df = self.parse_datetime(df)
        
        # Add features
        df = self.add_features(df)
        
        print(f"\nFinal dataset: {len(df)} rows")
        print(f"Columns: {', '.join(df.columns)}")
        
        # Save if output path provided
        if output_path:
            df.to_csv(output_path, index=False)
            print(f"\nSaved processed data to {output_path}")
        
        print("=" * 50)
        print("Data Preparation Complete")
        print("=" * 50)
        
        return df


def main():
    """Command-line interface for data preparation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Prepare Twitter data for sentiment analysis')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file path')
    parser.add_argument('--output', '-o', help='Output CSV file path')
    
    args = parser.parse_args()
    
    preparator = DataPreparator()
    df = preparator.prepare_data(args.input, args.output)
    
    # Display summary statistics
    print("\n" + "=" * 50)
    print("Data Summary")
    print("=" * 50)
    print(f"Total tweets: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else "")
    print(f"Average word count: {df['word_count'].mean():.1f}" if 'word_count' in df.columns else "")
    print(f"Retweets: {df['is_retweet'].sum()}" if 'is_retweet' in df.columns else "")


if __name__ == "__main__":
    main()
