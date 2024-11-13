from transformers import pipeline

sentiment_analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

def get_sentiment_for_paper(paper_text):
    sentiment = sentiment_analyzer(paper_text)
    return sentiment[0]['label']  # 'LABEL_0' for negative, 'LABEL_1' for neutral, 'LABEL_2' for positive

# Filter papers by keyword (e.g., stellarators, SPARC)
keywords = ['stellarator', 'SPARC', 'fusion breakthrough']

def get_papers_by_keyword(papers, keywords):
    keyword_papers = {}
    for filename, paper in papers.items():
        if any(keyword.lower() in paper['text'].lower() for keyword in keywords):
            keyword_papers[filename] = paper
    return keyword_papers

filtered_papers = get_papers_by_keyword(papers, keywords)
sentiments = {filename: get_sentiment_for_paper(paper['text']) for filename, paper in filtered_papers.items()}
