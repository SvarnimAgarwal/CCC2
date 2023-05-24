import couchdb
import pandas as pd
import re
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
#nltk.download('stopwords')
#nltk.download('punkt')
import time
import os

# Connect to CouchDB server
couch = couchdb.Server('http://admin:admin@172.26.134.93:5984/')

# Select the database
db = couch['mastodon_tooth']

# Define the Mango query with specific fields
query = {
    "selector": {},
    "limit": 400000,
    "fields": ["_id", "content"]
}

# Function for content cleaning and stemming
def clean_and_stem(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    stemmer = PorterStemmer()
    return ' '.join([stemmer.stem(word) for word in text.split()])

# Define the keywords
keywords = [
    "ufo", "alien", "aliens", "ufos", "flying saucer", "unidentified flying object", "alien spacecraft",
    "saucer", "flying object", "extraterrestrial", "crop circles", "alien encounter", "alien encounters",
    "unexplained phenomena", "flying disk", "celestial object", "#ufo", "#alien", "#aliens", "#ufos",
    "#flying saucer", "#unidentified flying object", "#alien spacecraft", "#saucer", "#flying object",
    "#extraterrestrial", "#crop circles", "#alien encounter", "#alien encounters", "#unexplained phenomena",
    "#flying disk", "#celestial object"
]

def update_wordcloud():
    # Retrieve the initial set of documents
    result = db.find(query)
    documents = [doc for doc in result]

    # Create a DataFrame from the list of documents
    df = pd.DataFrame(documents)

    # Apply content cleaning and stemming to the initial set of documents
    df['content'] = df['content'].apply(clean_and_stem)

    # Generate word cloud
    wordcloud_text = ' '.join(df['content'])
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Greens').generate(wordcloud_text)

    # Save the word cloud image
    wordcloud.to_file('static/wordcloudmastodon.png')

def update_stats():
    # Retrieve the initial set of documents
    result = db.find(query)
    documents = [doc for doc in result]

    # Create a DataFrame from the list of documents
    df = pd.DataFrame(documents)

    # Apply content cleaning and stemming to the initial set of documents
    df['content'] = df['content'].apply(clean_and_stem)

    # Print DataFrame information
    print(df.info())

    # Perform keyword counting
    counts = {}
    for keyword in keywords:
        counts[keyword] = df['content'].str.contains(r'\b{}\b'.format(keyword)).sum()

    # Calculate total number of documents
    total_docs = len(df)

    # Calculate the ratio of hits with keywords
    total_hits = sum(counts.values())
    ratio = (total_hits / total_docs) * 100

    # Save stats to a file
    stats_file = 'static/stats.txt'
    if not os.path.exists(stats_file):
        with open(stats_file, 'w') as f:
            f.write(str(total_docs) + '\n')
            f.write(str(ratio))
    else:
        with open(stats_file, 'r+') as f:
            lines = f.readlines()
            lines[0] = str(total_docs) + '\n'
            lines[1] = str(ratio)
            f.seek(0)
            f.writelines(lines)
            f.truncate()

    print('Stats updated.')

if __name__ == "__main__":
    while True:
        update_wordcloud()
        update_stats()
        time.sleep(60)
