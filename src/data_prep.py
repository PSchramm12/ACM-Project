"""
Data preparation script for Twitter data.
Converts CSV files into clean pandas DataFrames with all relevant tweet data preserved.
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path


def extract_hashtags(text):
    """
    Extract hashtags from text and return as a list.
    
    Parameters:
    -----------
    text : str
        Text to extract hashtags from
    
    Returns:
    --------
    list
        List of hashtags (with # symbol)
    """
    if pd.isna(text):
        return []
    
    text = str(text)
    # Extract hashtags using regex pattern #\w+
    hashtags = re.findall(r'#\w+', text)
    return hashtags


def parse_hashtags_column(hashtags_value):
    """
    Parse hashtags column value into a list format.
    Handles various formats: comma-separated strings, JSON arrays, etc.
    
    Parameters:
    -----------
    hashtags_value : str, list, or other
        Hashtags value from CSV column
    
    Returns:
    --------
    list
        List of hashtags
    """
    if pd.isna(hashtags_value):
        return []
    
    # If already a list, return as is
    if isinstance(hashtags_value, list):
        return hashtags_value
    
    # Convert to string
    hashtags_str = str(hashtags_value).strip()
    
    if not hashtags_str or hashtags_str.lower() in ['nan', 'none', '']:
        return []
    
    # Try to parse as JSON array if it looks like one
    if hashtags_str.startswith('[') and hashtags_str.endswith(']'):
        try:
            import json
            parsed = json.loads(hashtags_str)
            if isinstance(parsed, list):
                return parsed
        except:
            pass
    
    # Try comma-separated values
    if ',' in hashtags_str:
        hashtags = [h.strip() for h in hashtags_str.split(',')]
        # Ensure hashtags start with #
        hashtags = [h if h.startswith('#') else f'#{h}' for h in hashtags if h]
        return hashtags
    
    # Single hashtag
    if hashtags_str.startswith('#'):
        return [hashtags_str]
    
    return []


def load_twitter_data(file_path, label=None):
    """
    Load Twitter CSV file and return clean DataFrame with all relevant data preserved.
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the CSV file
    label : str, optional
        Label to add to the dataset (e.g., 'biden' or 'trump')
    
    Returns:
    --------
    pd.DataFrame
        Clean DataFrame with Twitter data, hashtags as lists
    """
    print(f"Loading {file_path}...")
    
    # Read CSV file
    # Use engine='python' for better error handling with large/malformed files
    # on_bad_lines='skip' will skip problematic rows instead of crashing
    try:
        df = pd.read_csv(
            file_path,
            engine='python',
            on_bad_lines='skip',
            encoding='utf-8',
            low_memory=True
        )
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        print("UTF-8 encoding failed, trying latin-1...")
        df = pd.read_csv(
            file_path,
            engine='python',
            on_bad_lines='skip',
            encoding='latin-1',
            low_memory=True
        )
    
    print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    print(f"Columns: {df.columns.tolist()}")
    
    # Parse datetime columns if they exist
    datetime_columns = ['created_at', 'tweet_created', 'date', 'timestamp']
    for col in datetime_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                print(f"Parsed datetime column: {col}")
            except Exception as e:
                print(f"Warning: Could not parse {col} as datetime: {e}")
    
    # Find text column (try common column names)
    text_columns = ['text', 'tweet', 'content', 'message']
    text_col = None
    for col in text_columns:
        if col in df.columns:
            text_col = col
            break
    
    # Handle hashtags column
    hashtag_columns = ['hashtags', 'hashtag', 'tags']
    existing_hashtag_col = None
    for col in hashtag_columns:
        if col in df.columns:
            existing_hashtag_col = col
            break
    
    if existing_hashtag_col:
        print(f"Found existing hashtags column: {existing_hashtag_col}")
        # Convert existing hashtags column to list format
        df['hashtags'] = df[existing_hashtag_col].apply(parse_hashtags_column)
        print("Converted hashtags column to list format")
    elif text_col:
        # Extract hashtags from text column
        print(f"Extracting hashtags from text column: {text_col}")
        df['hashtags'] = df[text_col].apply(extract_hashtags)
        print("Extracted hashtags from text")
    else:
        print("Warning: No text column found. Cannot extract hashtags.")
        df['hashtags'] = [[]] * len(df)
    
    # Only drop rows with completely missing text
    if text_col:
        df = df.dropna(subset=[text_col])
        # Also remove rows where text is empty string
        df = df[df[text_col].astype(str).str.strip().str.len() > 0].copy()
        print(f"After removing rows with missing/empty text: {len(df)} rows remaining")
    
    # Add label if provided
    if label:
        df['label'] = label
    
    return df


def merge_and_deduplicate(biden_df, trump_df):
    """
    Merge two Twitter DataFrames and remove duplicate tweets.
    
    Parameters:
    -----------
    biden_df : pd.DataFrame
        DataFrame with Biden tweets
    trump_df : pd.DataFrame
        DataFrame with Trump tweets
    
    Returns:
    --------
    pd.DataFrame
        Merged and deduplicated DataFrame
    """
    print("\nMerging datasets...")
    # Concatenate the two DataFrames
    merged_df = pd.concat([biden_df, trump_df], ignore_index=True)
    original_count = len(merged_df)
    print(f"Total rows before deduplication: {original_count}")
    
    # Find tweet ID column (check common names)
    id_columns = ['tweet_id', 'id', 'tweetId', 'status_id', 'tweetid']
    id_col = None
    for col in id_columns:
        if col in merged_df.columns:
            id_col = col
            print(f"Found tweet ID column: {col}")
            break
    
    # Find text column for text-based deduplication
    text_columns = ['text', 'tweet', 'content', 'message']
    text_col = None
    for col in text_columns:
        if col in merged_df.columns:
            text_col = col
            break
    
    # Remove duplicates
    if id_col:
        # Use tweet ID for deduplication
        print(f"Removing duplicates based on tweet ID ({id_col})...")
        merged_df = merged_df.drop_duplicates(subset=[id_col], keep='first')
        duplicates_removed = original_count - len(merged_df)
        print(f"Removed {duplicates_removed} duplicate tweets based on ID")
        
        # Also check for text duplicates among remaining rows
        if text_col:
            before_text_dedup = len(merged_df)
            # Normalize text for comparison (lowercase, strip whitespace)
            merged_df['_text_normalized'] = merged_df[text_col].astype(str).str.lower().str.strip()
            merged_df = merged_df.drop_duplicates(subset=['_text_normalized'], keep='first')
            merged_df = merged_df.drop(columns=['_text_normalized'])
            text_duplicates = before_text_dedup - len(merged_df)
            if text_duplicates > 0:
                print(f"Removed additional {text_duplicates} duplicate tweets based on text content")
                duplicates_removed += text_duplicates
    elif text_col:
        # Use text content for deduplication (case-insensitive)
        print(f"Removing duplicates based on text content ({text_col})...")
        # Normalize text for comparison
        merged_df['_text_normalized'] = merged_df[text_col].astype(str).str.lower().str.strip()
        merged_df = merged_df.drop_duplicates(subset=['_text_normalized'], keep='first')
        merged_df = merged_df.drop(columns=['_text_normalized'])
        duplicates_removed = original_count - len(merged_df)
        print(f"Removed {duplicates_removed} duplicate tweets based on text content")
    else:
        print("Warning: No tweet ID or text column found. Cannot deduplicate.")
        duplicates_removed = 0
    
    print(f"Total rows after deduplication: {len(merged_df)}")
    print(f"Total duplicates removed: {duplicates_removed}")
    
    return merged_df


def save_merged_data(merged_df, output_path='Data/Twitter Data/all_twitter_data.csv'):
    """
    Save merged DataFrame to CSV file.
    
    Parameters:
    -----------
    merged_df : pd.DataFrame
        Merged DataFrame to save
    output_path : str or Path
        Path to save the CSV file
    """
    output_path = Path(output_path)
    print(f"\nSaving merged dataset to {output_path}...")
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert list columns to string representation for CSV compatibility
    # Pandas can't directly save lists to CSV, so we'll convert them
    df_to_save = merged_df.copy()
    
    # Convert list columns (like hashtags) to string representation
    for col in df_to_save.columns:
        if df_to_save[col].dtype == object:
            # Check if column contains lists
            non_null_values = df_to_save[col].dropna()
            if len(non_null_values) > 0:
                sample_val = non_null_values.iloc[0]
                if isinstance(sample_val, list):
                    # Convert lists to JSON string representation
                    import json
                    df_to_save[col] = df_to_save[col].apply(
                        lambda x: json.dumps(x) if isinstance(x, list) else x
                    )
    
    # Save to CSV
    df_to_save.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Successfully saved {len(merged_df)} rows to {output_path}")


def prepare_dataframes(data_dir='Data/Twitter Data'):
    """
    Load and prepare both Twitter datasets into clean pandas DataFrames.
    
    Parameters:
    -----------
    data_dir : str or Path
        Directory containing the CSV files
    
    Returns:
    --------
    tuple
        (biden_df, trump_df)
        - biden_df: DataFrame for Biden tweets
        - trump_df: DataFrame for Trump tweets
    """
    data_path = Path(data_dir)
    
    # Load Biden dataset
    biden_file = data_path / 'hashtag_joebiden.csv'
    biden_df = load_twitter_data(biden_file, label='biden')
    
    # Load Trump dataset
    trump_file = data_path / 'hashtag_donaldtrump.csv'
    trump_df = load_twitter_data(trump_file, label='trump')
    
    # Merge and deduplicate datasets
    merged_df = merge_and_deduplicate(biden_df, trump_df)
    
    # Save merged dataset
    output_file = data_path / 'all_twitter_data.csv'
    save_merged_data(merged_df, output_file)
    
    # Basic statistics
    print("\n" + "="*50)
    print("Dataset Statistics:")
    print("="*50)
    print(f"Biden tweets: {len(biden_df)}")
    print(f"Trump tweets: {len(trump_df)}")
    print(f"Total tweets before merge: {len(biden_df) + len(trump_df)}")
    print(f"Merged tweets (after deduplication): {len(merged_df)}")
    print(f"Duplicates removed: {len(biden_df) + len(trump_df) - len(merged_df)}")
    
    # Find text column for statistics
    text_columns = ['text', 'tweet', 'content', 'message']
    text_col = None
    for col in text_columns:
        if col in biden_df.columns:
            text_col = col
            break
    
    if text_col:
        print(f"\nAverage text length:")
        print(f"  Biden: {biden_df[text_col].astype(str).str.len().mean():.1f} characters")
        print(f"  Trump: {trump_df[text_col].astype(str).str.len().mean():.1f} characters")
    
    # Check hashtags statistics
    if 'hashtags' in biden_df.columns:
        print(f"\nHashtags statistics:")
        biden_hashtag_counts = biden_df['hashtags'].apply(len)
        trump_hashtag_counts = trump_df['hashtags'].apply(len)
        print(f"  Biden: avg {biden_hashtag_counts.mean():.2f} hashtags per tweet")
        print(f"  Trump: avg {trump_hashtag_counts.mean():.2f} hashtags per tweet")
    
    # Check for common Twitter metrics
    metric_cols = ['retweet_count', 'favorite_count', 'like_count', 'reply_count']
    available_metrics = [col for col in metric_cols if col in biden_df.columns]
    if available_metrics:
        print(f"\nAvailable engagement metrics: {available_metrics}")
        for col in available_metrics:
            print(f"  {col}:")
            print(f"    Biden - mean={biden_df[col].mean():.2f}, median={biden_df[col].median():.2f}")
            print(f"    Trump - mean={trump_df[col].mean():.2f}, median={trump_df[col].median():.2f}")
    
    print("="*50 + "\n")
    
    return biden_df, trump_df


if __name__ == "__main__":
    # Load and prepare the dataframes
    biden_df, trump_df = prepare_dataframes()
    
    # Display sample data
    print("Sample from Biden dataset:")
    print(biden_df.head())
    print("\nSample from Trump dataset:")
    print(trump_df.head())
    
    # Display column information
    print("\n" + "="*50)
    print("DataFrame Info:")
    print("="*50)
    print("\nBiden DataFrame columns:")
    print(biden_df.columns.tolist())
    print("\nTrump DataFrame columns:")
    print(trump_df.columns.tolist())
    print("="*50)
