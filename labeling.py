#### MANUAL LABELING EXAMPLE ####
#################################
# This file contains an example of how you might manually label a small dataset of papers.
# In practice, you would likely use a larger dataset and possibly automate the labeling process.
# For simplicity, we're using a small manual dataset and a simple function to retrieve sentiment labels.

# Example labeled dataset for sentiment
# This is a small example dataset, you'd manually label a larger portion
manual_labels = {
    "paper1.pdf": "positive",   # Paper with an optimistic tone or breakthrough
    "paper2.pdf": "neutral",    # Paper is purely informative, no strong sentiment
    "paper3.pdf": "negative",   # Paper discusses significant challenges or limitations
}

# Function to retrieve sentiment label (for small manual dataset)
def get_sentiment_label(paper_text, paper_filename):
    """
    Given the paper text and filename, this function assigns a sentiment label.
    In this example, it's using manually labeled papers (you'll need to expand this).
    """
    if paper_filename in manual_labels:
        return manual_labels[paper_filename]
    else:
        # If not manually labeled, you could apply VADER/TextBlob here as a fallback
        # For now, we just return a default label (neutral).
        return "neutral"
    
    
#### VADER SENTIMENT ANALYSIS ####
#################################
# This file contains a simple sentiment analysis function using VADER (Valence Aware Dictionary and sEntiment Reasoner).
# VADER is a lexicon and rule-based sentiment analysis tool specifically designed for social media.
# It's particularly good at handling social media texts, emojis, and informal language.

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_label_vader(paper_text):
    """
    Assign sentiment label (positive, neutral, or negative) using VADER.
    """
    sentiment_score = analyzer.polarity_scores(paper_text)['compound']
    
    if sentiment_score >= 0.05:
        return "positive"
    elif sentiment_score <= -0.05:
        return "negative"
    else:
        return "neutral"

#### TEXTBLOB SENTIMENT ANALYSIS ####
#####################################
# This file contains a simple sentiment analysis function using TextBlob.
# TextBlob is a Python library for processing textual data. It provides a simple API for common natural language processing (NLP) tasks.
# TextBlob's sentiment analysis uses a lexicon-based approach.

from textblob import TextBlob

def get_sentiment_label_textblob(paper_text):
    """
    Assign sentiment label using TextBlob.
    """
    # Calculate the polarity score (ranging from -1 to 1)
    blob = TextBlob(paper_text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

#### AUTOMATIC LABELING EXAMPLE ####
###################################
# This file contains an example of how you might automatically label a collection of papers using VADER or TextBlob.
# In practice, you might use a more sophisticated model or ensemble of models for sentiment analysis.
# For simplicity, we're using VADER and TextBlob for automatic labeling.
# You would typically use a larger dataset and more advanced models for real-world applications.
# The sentiment labels can be used for further analysis, visualization, or categorization of papers.
# This example assumes you have a collection of papers with text content.
# The sentiment labels are added to the paper dictionary for further processing.

# Example: Automatic labeling for a collection of papers
for filename, paper in papers.items():
    paper_text = paper['text']  # Assuming 'text' contains the full text or abstract
    # Use VADER or TextBlob for automatic sentiment labeling
    sentiment = get_sentiment_label_vader(paper_text)  # or get_sentiment_label_textblob()
    paper['sentiment'] = sentiment  # Add the sentiment label to the paper dictionary

# Example output
for filename, paper in papers.items():
    print(f"Paper: {filename}, Sentiment: {paper['sentiment']}")
