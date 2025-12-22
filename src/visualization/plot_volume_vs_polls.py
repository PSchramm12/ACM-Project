"""
Visualization Module - Tweet Volume vs Polling Data

This module creates visualizations comparing tweet volume over time with polling data.

Author: Tyler
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


class TweetVolumeAnalyzer:
    """Analyze and visualize tweet volume over time against polling data."""
    
    def __init__(self):
        """Initialize the analyzer."""
        pass
    
    def aggregate_tweet_volume(self, 
                              df: pd.DataFrame, 
                              date_column: str = 'date',
                              freq: str = 'D') -> pd.DataFrame:
        """
        Aggregate tweet volume by time period.
        
        Args:
            df: DataFrame with tweets
            date_column: Name of date column
            freq: Frequency for aggregation ('D'=daily, 'W'=weekly, 'M'=monthly)
            
        Returns:
            DataFrame with aggregated tweet counts
        """
        df[date_column] = pd.to_datetime(df[date_column])
        volume = df.groupby(pd.Grouper(key=date_column, freq=freq)).size().reset_index(name='tweet_count')
        volume.columns = ['date', 'tweet_count']
        return volume
    
    def load_polling_data(self, filepath: str) -> pd.DataFrame:
        """
        Load polling data from CSV.
        
        Expected columns:
        - date: Date of poll
        - poll_value: Polling value (e.g., approval rating, candidate support %)
        - poll_name: Name of poll or candidate (optional)
        
        Args:
            filepath: Path to polling data CSV
            
        Returns:
            DataFrame with polling data
        """
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def merge_data(self, 
                  tweet_volume: pd.DataFrame, 
                  polling_data: pd.DataFrame) -> pd.DataFrame:
        """
        Merge tweet volume and polling data.
        
        Args:
            tweet_volume: DataFrame with tweet counts
            polling_data: DataFrame with polling data
            
        Returns:
            Merged DataFrame
        """
        merged = pd.merge(tweet_volume, polling_data, on='date', how='outer')
        merged = merged.sort_values('date')
        return merged
    
    def plot_volume_vs_polls(self,
                            tweet_volume: pd.DataFrame,
                            polling_data: pd.DataFrame,
                            output_path: Optional[str] = None,
                            title: str = "Tweet Volume vs Polling Data") -> None:
        """
        Create dual-axis plot of tweet volume and polling data.
        
        Args:
            tweet_volume: DataFrame with date and tweet_count columns
            polling_data: DataFrame with date and poll_value columns
            output_path: Path to save figure (optional)
            title: Plot title
        """
        fig, ax1 = plt.subplots(figsize=(14, 8))
        
        # Plot tweet volume on left axis
        color1 = 'tab:blue'
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Tweet Volume', color=color1, fontsize=12)
        ax1.plot(tweet_volume['date'], tweet_volume['tweet_count'], 
                color=color1, linewidth=2, label='Tweet Volume')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(True, alpha=0.3)
        
        # Plot polling data on right axis
        ax2 = ax1.twinx()
        color2 = 'tab:red'
        ax2.set_ylabel('Polling Value (%)', color=color2, fontsize=12)
        ax2.plot(polling_data['date'], polling_data['poll_value'], 
                color=color2, linewidth=2, linestyle='--', label='Polling Data')
        ax2.tick_params(axis='y', labelcolor=color2)
        
        # Title and legend
        plt.title(title, fontsize=14, fontweight='bold')
        
        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {output_path}")
        
        plt.show()
    
    def plot_sentiment_volume_vs_polls(self,
                                      df: pd.DataFrame,
                                      polling_data: pd.DataFrame,
                                      date_column: str = 'date',
                                      sentiment_column: str = 'sentiment',
                                      output_path: Optional[str] = None) -> None:
        """
        Create stacked area plot of sentiment volume vs polling data.
        
        Args:
            df: DataFrame with tweets including sentiment
            polling_data: DataFrame with polling data
            date_column: Name of date column
            sentiment_column: Name of sentiment column
            output_path: Path to save figure (optional)
        """
        # Aggregate by date and sentiment
        df[date_column] = pd.to_datetime(df[date_column])
        sentiment_volume = df.groupby([pd.Grouper(key=date_column, freq='D'), 
                                       sentiment_column]).size().unstack(fill_value=0)
        
        fig, ax1 = plt.subplots(figsize=(14, 8))
        
        # Create stacked area plot
        colors = {'positive': '#2ecc71', 'neutral': '#95a5a6', 'negative': '#e74c3c'}
        sentiment_volume.plot.area(ax=ax1, color=[colors.get(x, '#3498db') for x in sentiment_volume.columns],
                                  alpha=0.7, linewidth=0)
        
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Tweet Volume by Sentiment', fontsize=12)
        ax1.legend(title='Sentiment', loc='upper left')
        
        # Add polling data on secondary axis
        ax2 = ax1.twinx()
        ax2.plot(polling_data['date'], polling_data['poll_value'],
                color='black', linewidth=2, linestyle='--', label='Polling Data', marker='o')
        ax2.set_ylabel('Polling Value (%)', fontsize=12)
        ax2.legend(loc='upper right')
        
        plt.title('Tweet Sentiment Volume vs Polling Data Over Time', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {output_path}")
        
        plt.show()
    
    def calculate_correlation(self, 
                            tweet_volume: pd.DataFrame,
                            polling_data: pd.DataFrame) -> float:
        """
        Calculate correlation between tweet volume and polling data.
        
        Args:
            tweet_volume: DataFrame with tweet counts
            polling_data: DataFrame with polling data
            
        Returns:
            Correlation coefficient
        """
        merged = self.merge_data(tweet_volume, polling_data)
        merged = merged.dropna()
        
        if len(merged) < 2:
            print("Not enough data points for correlation")
            return 0.0
        
        corr = merged['tweet_count'].corr(merged['poll_value'])
        return corr


def main():
    """Command-line interface for volume vs polls visualization."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Plot tweet volume vs polling data')
    parser.add_argument('--tweets', '-t', required=True, help='Tweet data CSV file')
    parser.add_argument('--polls', '-p', required=True, help='Polling data CSV file')
    parser.add_argument('--output', '-o', help='Output image file path')
    parser.add_argument('--freq', default='D', choices=['D', 'W', 'M'], 
                       help='Aggregation frequency (D=daily, W=weekly, M=monthly)')
    parser.add_argument('--sentiment', action='store_true', 
                       help='Include sentiment breakdown in visualization')
    
    args = parser.parse_args()
    
    analyzer = TweetVolumeAnalyzer()
    
    # Load data
    print(f"Loading tweet data from {args.tweets}...")
    tweets_df = pd.read_csv(args.tweets)
    
    print(f"Loading polling data from {args.polls}...")
    polling_df = analyzer.load_polling_data(args.polls)
    
    if args.sentiment and 'sentiment' in tweets_df.columns:
        # Create sentiment-based visualization
        analyzer.plot_sentiment_volume_vs_polls(tweets_df, polling_df, output_path=args.output)
    else:
        # Aggregate tweet volume
        tweet_volume = analyzer.aggregate_tweet_volume(tweets_df, freq=args.freq)
        
        # Create visualization
        analyzer.plot_volume_vs_polls(tweet_volume, polling_df, output_path=args.output)
        
        # Calculate correlation
        corr = analyzer.calculate_correlation(tweet_volume, polling_df)
        print(f"\nCorrelation between tweet volume and polling data: {corr:.3f}")


if __name__ == "__main__":
    main()
