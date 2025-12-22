# Quick Start Guide

## For Team Members

### Nicolai - Tasks from Slides & Topic Sentiment Analysis

Your tasks:
1. Review `docs/tasks_from_slides.md` and fill in answers to research questions
2. Work with Pascal on topic-specific sentiment analysis using `src/sentiment/analyze_sentiment.py`
3. Focus on migration, Texas, and other policy topics

Quick command to analyze topic sentiment:
```bash
python src/sentiment/analyze_sentiment.py \
    --input data/processed/tweets_clean.csv \
    --output output/topic_sentiment_results.csv \
    --topics
```

### Pascal - Data Preparation & Sentiment Analysis

Your tasks:
1. Implement data collection pipeline
2. Run data preparation: `python src/data_preparation/prepare_data.py -i data/raw/tweets.csv -o data/processed/tweets_clean.csv`
3. Run sentiment analysis: `python src/sentiment/analyze_sentiment.py -i data/processed/tweets_clean.csv -o data/processed/tweets_with_sentiment.csv --topics`
4. Work on sentiment clustering (to be implemented)

Your main files:
- `src/data_preparation/prepare_data.py`
- `src/sentiment/analyze_sentiment.py`
- `notebooks/02_sentiment_analysis.ipynb`

### Tyler - Visualization & Plotting

Your tasks:
1. Create visualizations comparing tweet volume with polling data
2. Implement time series plots
3. Generate correlation analysis

Your main files:
- `src/visualization/plot_volume_vs_polls.py`

Quick command:
```bash
python src/visualization/plot_volume_vs_polls.py \
    --tweets data/processed/tweets_with_sentiment.csv \
    --polls data/raw/polling_data.csv \
    --output output/volume_vs_polls.png \
    --sentiment
```

### Jacob - Literature Research

Your tasks:
1. Fill in `docs/literature_research.md` with relevant papers
2. Research sentiment analysis methodologies
3. Find papers on social media and polling correlation
4. Document best practices and relevant findings

Your main file:
- `docs/literature_research.md`

## Common Commands

### Setup (Everyone)
```bash
# Clone and setup
git clone https://github.com/PSchramm12/ACM-Project.git
cd ACM-Project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install project in development mode (optional but recommended)
pip install -e .

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

### Data Pipeline
```bash
# 1. Prepare data (Pascal)
python src/data_preparation/prepare_data.py -i data/raw/tweets.csv -o data/processed/tweets_clean.csv

# 2. Analyze sentiment (Pascal)
python src/sentiment/analyze_sentiment.py -i data/processed/tweets_clean.csv -o data/processed/tweets_with_sentiment.csv --topics

# 3. Create visualizations (Tyler)
python src/visualization/plot_volume_vs_polls.py -t data/processed/tweets_with_sentiment.csv -p data/raw/polling_data.csv -o output/results.png --sentiment
```

### Testing
```bash
pip install pytest
python -m pytest tests/ -v
```

### Jupyter Notebooks
```bash
jupyter notebook
# Then open notebooks/01_data_exploration.ipynb or notebooks/02_sentiment_analysis.ipynb
```

## Data Format Requirements

### Tweet Data (CSV)
Required columns:
- `tweet_id`: Unique identifier
- `text`: Tweet text content
- `created_at`: Timestamp

### Polling Data (CSV)
Required columns:
- `date`: Date (YYYY-MM-DD)
- `poll_value`: Numeric value (e.g., percentage)

See `data/README.md` for detailed format specifications.

## Need Help?

1. Check `docs/PROJECT_GUIDE.md` for comprehensive documentation
2. Review module-specific READMEs in `src/` subdirectories
3. Look at example notebooks in `notebooks/`
4. Ask team members or create an issue on GitHub

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push and create PR
git push origin feature/your-feature-name
```
