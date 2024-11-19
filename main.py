import os
from extract_pdf import extract_text_from_pdf, extract_year_from_pdf, extract_title_from_pdf
from transformers import BertForSequenceClassification, BertTokenizer
import torch
import matplotlib.pyplot as plt
from collections import defaultdict

pdf_dir = "/Users/rogeriojorge/Dropbox/Papers_Read/Papers_To_Read"
papers = {}

## QUERY ARXIV FOR ALL STELLARATOR PAPERS

# Load the trained model and tokenizer
model = BertForSequenceClassification.from_pretrained("./trained_sentiment_model")
tokenizer = BertTokenizer.from_pretrained("./trained_sentiment_model")

def get_sentiment_label_bert(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    label_map = {0: "positive", 1: "neutral"}
    return label_map[prediction]

yearly_sentiment_counts = defaultdict(lambda: {"positive": 0, "neutral": 0})

for i, filename in enumerate(os.listdir(pdf_dir)):
    if filename.endswith('.pdf'):
        # print(filename)
        pdf_path = os.path.join(pdf_dir, filename)
        text = extract_text_from_pdf(pdf_path)
        # Extract metadata from PDF (e.g., year, title, abstract)
        # You can use pdfmetadata or regex to capture this info
        if 'stellarator' in text.lower():# and 'tokamak' in text.lower():
            papers[filename] = {
                'text': text,
                'year': extract_year_from_pdf(pdf_path),
                'title': extract_title_from_pdf(pdf_path),
                'filename': filename,
                'sentiment': get_sentiment_label_bert(text) # Predict sentiment using trained model
            }
            print(f"File: {papers[filename]['filename']}, Year: {papers[filename]['year']}, Title: {papers[filename]['title']}, Sentiment: {papers[filename]['sentiment']}")
            yearly_sentiment_counts[papers[filename]['year']][papers[filename]['sentiment']] += 1

years = sorted(yearly_sentiment_counts.keys())
positive_fractions = []

for year in years:
    total_papers = yearly_sentiment_counts[year]["positive"] + yearly_sentiment_counts[year]["neutral"]
    if total_papers > 0:
        positive_fraction = yearly_sentiment_counts[year]["positive"] / total_papers
    else:
        positive_fraction = 0
    positive_fractions.append(positive_fraction)

plt.figure(figsize=(10, 6))
plt.plot(years, positive_fractions, marker='o', color='b', linestyle='-')
plt.xlabel("Year")
plt.ylabel("Fraction of Positive Papers")
plt.title("Fraction of Positive Papers Over Time")
plt.grid(True)
plt.show()

# # Only print the first paper
# first_paper = list(papers.items())[1]
# print(first_paper)