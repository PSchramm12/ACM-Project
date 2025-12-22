# ACM Project Guide

## Project Overview

This project analyzes social media sentiment (primarily Twitter/X) in relation to political topics and polling data. The goal is to understand the relationship between online sentiment and public opinion as measured by polls.

## Team Structure

| Team Member | Responsibilities |
|-------------|------------------|
| **Nicolai** | - Check tasks from slides and prepare answers<br>- Topic-specific sentiment analysis (migration, Texas, etc.)<br>- Project coordination |
| **Pascal** | - Data preparation and cleaning<br>- Sentiment analysis implementation<br>- Sentiment clustering<br>- Topic-specific sentiment (with Nicolai) |
| **Tyler** | - Visualization development<br>- Tweet volume vs polling data plots<br>- Time series analysis |
| **Jacob** | - Literature research<br>- Theoretical framework<br>- Methodology documentation |

## Getting Started

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/PSchramm12/ACM-Project.git
cd ACM-Project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
```

### 2. Data Collection

See `data/README.md` for detailed instructions on:
- Collecting Twitter data
- Sourcing polling data
- Data format requirements

### 3. Workflow

```
Raw Data → Data Preparation → Sentiment Analysis → Visualization → Analysis
```

## Module Usage

### Data Preparation (Pascal)

```bash
# Clean and prepare tweet data
python src/data_preparation/prepare_data.py \
    --input data/raw/tweets.csv \
    --output data/processed/tweets_clean.csv
```

### Sentiment Analysis (Pascal)

```bash
# Perform sentiment analysis
python src/sentiment/analyze_sentiment.py \
    --input data/processed/tweets_clean.csv \
    --output data/processed/tweets_with_sentiment.csv \
    --topics
```

### Visualization (Tyler)

```bash
# Create volume vs polls visualization
python src/visualization/plot_volume_vs_polls.py \
    --tweets data/processed/tweets_with_sentiment.csv \
    --polls data/raw/polling_data.csv \
    --output output/volume_vs_polls.png \
    --sentiment
```

## Jupyter Notebooks

Exploratory analysis notebooks are available in the `notebooks/` directory:

1. `01_data_exploration.ipynb` - Initial data exploration
2. `02_sentiment_analysis.ipynb` - Sentiment analysis demonstration

To start Jupyter:
```bash
jupyter notebook
```

## Testing

Run unit tests:
```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_data_preparation.py -v
```

## Documentation

- `docs/tasks_from_slides.md` - Tasks and questions from project slides (Nicolai)
- `docs/literature_research.md` - Literature review and references (Jacob)
- Module READMEs in each `src/` subdirectory

## Research Questions

1. How does social media sentiment correlate with polling data?
2. What topics/policies generate the most engagement?
3. How does sentiment differ across specific policy areas?
4. Can we identify sentiment clusters or patterns?
5. What is the relationship between tweet volume and polling changes?

## Topics of Interest

- **Migration/Immigration**: Border policy, asylum, immigration reform
- **Texas-Specific Issues**: Regional political topics
- **Economy**: Inflation, jobs, economic policy
- **Healthcare**: Healthcare reform, insurance, Medicare
- **Climate**: Climate change, environmental policy
- **Education**: School policy, student issues

## Output Structure

```
output/
├── figures/              # Generated plots and visualizations
├── results/              # Analysis results and statistics
└── reports/              # Final reports and presentations
```

## Best Practices

1. **Version Control**
   - Commit frequently with descriptive messages
   - Use feature branches for major changes
   - Review code before merging

2. **Data Management**
   - Never commit raw data to git
   - Document data sources
   - Maintain data provenance

3. **Code Quality**
   - Follow PEP 8 style guidelines
   - Write docstrings for functions
   - Add unit tests for new features

4. **Documentation**
   - Update README when adding features
   - Document analysis decisions
   - Keep track of research findings

## Troubleshooting

### Import Errors
If you get import errors, make sure you're in the project root directory and the virtual environment is activated.

### NLTK Data Errors
Run: `python -c "import nltk; nltk.download('all')"`

### Memory Issues with Large Datasets
Process data in chunks using pandas `chunksize` parameter.

## Resources

- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [Tweepy Documentation](https://docs.tweepy.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

## Contact

For questions or issues, contact team members or create an issue in the GitHub repository.
