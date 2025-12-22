# ACM Social Media Sentiment Analysis Project

This project analyzes social media (Twitter) sentiment in relation to political topics and polling data.

## Team Members and Responsibilities

- **Nicolai**: Check tasks from Slides and prepare answers; Sentiment directed at specific policies/topics
- **Pascal**: Prepare Data for further analysis; Sentiment Clusters/Sentiment Analysis; Sentiment directed at specific policies/topics
- **Tyler**: Plotting tweet volume over time against polling data
- **Jacob**: Further Literature Research

## Project Structure

```
ACM-Project/
├── data/
│   ├── raw/              # Raw data files (not tracked in git)
│   └── processed/        # Processed/cleaned data (not tracked in git)
├── src/
│   ├── data_preparation/ # Data cleaning and preprocessing
│   ├── sentiment/        # Sentiment analysis modules
│   ├── visualization/    # Plotting and visualization
│   └── utils/            # Utility functions
├── notebooks/            # Jupyter notebooks for exploration
├── docs/                 # Documentation and literature research
├── output/               # Analysis outputs
└── tests/                # Unit tests
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/PSchramm12/ACM-Project.git
cd ACM-Project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```bash
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

## Data Preparation

See `src/data_preparation/README.md` for detailed instructions on preparing data for analysis.

## Usage

### Data Preparation
```bash
python src/data_preparation/prepare_data.py --input data/raw/tweets.csv --output data/processed/tweets_clean.csv
```

### Sentiment Analysis
```bash
python src/sentiment/analyze_sentiment.py --input data/processed/tweets_clean.csv --output output/sentiment_results.csv
```

### Visualization
```bash
python src/visualization/plot_volume_vs_polls.py --tweets data/processed/tweets_clean.csv --polls data/raw/polling_data.csv
```

## Contributing

When working on your assigned tasks:
1. Create a feature branch from `main`
2. Make your changes
3. Test your code
4. Submit a pull request

## License

This project is for academic purposes as part of an ACM (Association for Computing Machinery) project.