# Define a list of aspects/keywords that you want to analyze sentiment for
aspects = ["stellarator", "SPARC", "fusion breakthrough"]

import re
from nltk.tokenize import sent_tokenize

def extract_aspect_sentences(paper_text, aspect_keywords):
    """
    Extract sentences that contain any of the aspect-related keywords.
    """
    sentences = sent_tokenize(paper_text)  # Tokenize text into sentences
    aspect_sentences = []
    
    for sentence in sentences:
        if any(keyword.lower() in sentence.lower() for keyword in aspect_keywords):
            aspect_sentences.append(sentence)
    
    return aspect_sentences

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_label_vader(text):
    """
    Use VADER to return sentiment label for a given text.
    """
    sentiment_score = analyzer.polarity_scores(text)['compound']
    
    if sentiment_score >= 0.05:
        return "positive"
    elif sentiment_score <= -0.05:
        return "negative"
    else:
        return "neutral"

def aspect_based_sentiment_analysis(paper_text, aspects):
    """
    Perform aspect-based sentiment analysis for a given paper text.
    Returns a dictionary with sentiment for each aspect.
    """
    aspect_sentiments = {}

    for aspect in aspects:
        # Extract sentences related to the current aspect
        aspect_sentences = extract_aspect_sentences(paper_text, [aspect])
        
        # If no sentences were found for this aspect, continue
        if not aspect_sentences:
            aspect_sentiments[aspect] = "neutral"  # No sentiment found, default to neutral
            continue
        
        # Analyze sentiment for each sentence related to the aspect
        aspect_sentiment_scores = [get_sentiment_label_vader(sentence) for sentence in aspect_sentences]
        
        # Aggregate the sentiment scores for the aspect (simple majority rule)
        positive_count = aspect_sentiment_scores.count("positive")
        negative_count = aspect_sentiment_scores.count("negative")
        neutral_count = aspect_sentiment_scores.count("neutral")
        
        # Set the final sentiment for the aspect (based on majority)
        if positive_count > negative_count and positive_count > neutral_count:
            aspect_sentiments[aspect] = "positive"
        elif negative_count > positive_count and negative_count > neutral_count:
            aspect_sentiments[aspect] = "negative"
        else:
            aspect_sentiments[aspect] = "neutral"
    
    return aspect_sentiments

# Example usage: Apply ABSA to a collection of papers
aspect_sentiment_results = {}

# Example list of paper files and their text (you would load this from your actual data)
papers = {
    "paper1.pdf": {"text": "The stellarator design is promising, but challenges remain."},
    "paper2.pdf": {"text": "SPARC has made remarkable progress towards achieving net-positive energy."},
    "paper3.pdf": {"text": "There has been little progress on stellarator technology."},
}

for filename, paper in papers.items():
    paper_text = paper['text']
    
    # Perform aspect-based sentiment analysis on the paper text
    sentiment = aspect_based_sentiment_analysis(paper_text, aspects)
    
    # Store the results (this will be a dictionary mapping aspect to sentiment)
    aspect_sentiment_results[filename] = sentiment

# Print the results for each paper
for filename, sentiment in aspect_sentiment_results.items():
    print(f"Paper: {filename}")
    for aspect, sentiment_label in sentiment.items():
        print(f"  Aspect: {aspect}, Sentiment: {sentiment_label}")

import matplotlib.pyplot as plt
import pandas as pd

# Sample data: Aspect sentiment over years
sentiment_data = [
    {"year": 2019, "aspect": "stellarator", "sentiment": "neutral"},
    {"year": 2020, "aspect": "stellarator", "sentiment": "positive"},
    {"year": 2021, "aspect": "stellarator", "sentiment": "negative"},
    {"year": 2020, "aspect": "SPARC", "sentiment": "positive"},
    {"year": 2021, "aspect": "SPARC", "sentiment": "positive"},
]

df = pd.DataFrame(sentiment_data)

# Convert sentiment to numerical values (positive=1, neutral=0, negative=-1)
sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
df['sentiment_score'] = df['sentiment'].map(sentiment_map)

# Plot sentiment over time for each aspect
plt.figure(figsize=(10, 6))
for aspect in df['aspect'].unique():
    aspect_data = df[df['aspect'] == aspect]
    plt.plot(aspect_data['year'], aspect_data['sentiment_score'], marker='o', label=aspect)

plt.title("Aspect-Based Sentiment Over Time")
plt.xlabel("Year")
plt.ylabel("Sentiment Score")
plt.legend()
plt.grid(True)
plt.show()
