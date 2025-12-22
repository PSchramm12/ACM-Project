# Visualization Module

This module provides visualization tools for analyzing tweet data and polling data.

## Responsibilities (Tyler)

1. **Tweet Volume Over Time**: Plot tweet volume trends
2. **Polling Data Visualization**: Display polling data trends
3. **Combined Visualizations**: Compare tweet volume with polling data
4. **Sentiment-Based Visualizations**: Show sentiment distribution over time

## Files

- `plot_volume_vs_polls.py`: Main script for volume vs polling visualization
- `time_series_plots.py`: Time series visualization utilities
- `correlation_analysis.py`: Statistical correlation analysis

## Usage

### Basic Volume vs Polls Plot

```bash
python src/visualization/plot_volume_vs_polls.py \
    --tweets data/processed/tweets_clean.csv \
    --polls data/raw/polling_data.csv \
    --output output/volume_vs_polls.png
```

### With Sentiment Breakdown

```bash
python src/visualization/plot_volume_vs_polls.py \
    --tweets data/processed/tweets_with_sentiment.csv \
    --polls data/raw/polling_data.csv \
    --sentiment \
    --output output/sentiment_volume_vs_polls.png
```

### Weekly Aggregation

```bash
python src/visualization/plot_volume_vs_polls.py \
    --tweets data/processed/tweets_clean.csv \
    --polls data/raw/polling_data.csv \
    --freq W \
    --output output/weekly_volume_vs_polls.png
```

## Polling Data Format

The polling data CSV should have the following columns:

```csv
date,poll_value,poll_name
2024-01-01,45.2,Approval Rating
2024-01-02,45.5,Approval Rating
2024-01-03,44.8,Approval Rating
```

- `date`: Date of the poll (YYYY-MM-DD format)
- `poll_value`: Numeric polling value (e.g., percentage)
- `poll_name`: Name of the poll or candidate (optional)

## Visualization Features

1. **Dual-Axis Plots**: Tweet volume on left axis, polling data on right axis
2. **Stacked Area Charts**: Sentiment breakdown over time
3. **Correlation Analysis**: Calculate correlation between tweet volume and polls
4. **Interactive Plots**: Optional Plotly support for interactive visualizations

## Example Output

The visualization will show:
- Blue line: Tweet volume over time
- Red dashed line: Polling data over time
- Grid for easy reading
- Legend identifying each line
- Correlation coefficient in output
