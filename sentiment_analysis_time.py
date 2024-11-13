import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame with year and sentiment data
sentiment_data = []
for filename, paper in filtered_papers.items():
    sentiment = get_sentiment_for_paper(paper['text'])
    sentiment_data.append({
        'year': paper['year'],
        'sentiment': sentiment
    })

df = pd.DataFrame(sentiment_data)

# Convert sentiment to numerical values for analysis
sentiment_map = {'LABEL_0': -1, 'LABEL_1': 0, 'LABEL_2': 1}
df['sentiment_score'] = df['sentiment'].map(sentiment_map)

# Group by year and calculate average sentiment score
yearly_sentiment = df.groupby('year')['sentiment_score'].mean().reset_index()

# Plot sentiment over time
plt.figure(figsize=(10, 6))
plt.plot(yearly_sentiment['year'], yearly_sentiment['sentiment_score'], marker='o')
plt.title('Sentiment Towards Fusion Research (2010 - Present)')
plt.xlabel('Year')
plt.ylabel('Average Sentiment')
plt.grid(True)
plt.show()

# Look for sudden increases in positive sentiment
def identify_sentiment_spikes(df):
    df['diff'] = df['sentiment_score'].diff()
    spikes = df[df['diff'] > 0.5]  # You can adjust this threshold based on the magnitude of change
    return spikes

breakthrough_spikes = identify_sentiment_spikes(yearly_sentiment)
print(breakthrough_spikes)