import couchdb
import pandas as pd
import folium
from folium.plugins import HeatMap
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Connect to CouchDB server
couch = couchdb.Server('http://admin:admin@172.26.134.93:5984/')

# Select the database
db = couch['twitter-full-new']

# Define the Mango query with specific fields
query = {
    "selector": {},
    "fields": ["doc.data.author_id", "doc.data.geo", "doc.data.text", "doc.data.sentiment", "value.tokens", "doc.data.created_at", "doc.includes.places"],
    "limit": 200000
}

# Function to process a single document
def process_doc(doc):
    user_id = doc['doc']['data']['author_id']
    geo = doc['doc']['data']['geo']
    place_name = None
    bbox = None

    if 'includes' in doc['doc'] and 'places' in doc['doc']['includes']:
        places = doc['doc']['includes']['places']
        if len(places) > 0:
            place_name = places[0]['full_name']
            bbox = places[0]['geo'].get('bbox')

    text = doc['doc']['data']['text']
    sentiment = doc['doc']['data']['sentiment']
    token = doc['value']['tokens']
    created_at = doc['doc']['data']['created_at']

    return {
        'user_id': user_id,
        'bbox': bbox,
        'text': text,
        'sentiment': sentiment,
        'tokens': token,
        'created_at': created_at,
        'place_name': place_name
    }

# Fetch data using the query
result = db.find(query)
result = list(result)

# Process the data and store in a list
processed_data = []
for doc in result:
    processed_doc = process_doc(doc)
    processed_data.append(processed_doc)

# Create a DataFrame from the processed data
df = pd.DataFrame(processed_data)

# Filter out rows with missing bounding boxes and sentiment values
df = df.dropna(subset=['bbox', 'sentiment'])

def convert_bbox_to_lat_long(bbox):
    if len(bbox) == 4:
        lat = (bbox[1] + bbox[3]) / 2
        lon = (bbox[0] + bbox[2]) / 2
        return lat, lon
    else:
        return None, None

# Convert bbox to latitude and longitude coordinates
df['latitude'], df['longitude'] = zip(*df['bbox'].map(lambda bbox: convert_bbox_to_lat_long(bbox)))
# Filter out rows with missing latitude and longitude values
df = df.dropna(subset=['latitude', 'longitude'])

print(df.info())

# Preprocess and clean the text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # Join tokens back into text
    cleaned_text = ' '.join(tokens)
    return cleaned_text

df['cleaned_text'] = df['text'].apply(preprocess_text)

# Generate a word cloud
text = ' '.join(df['cleaned_text'].tolist())

wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Greens', contour_color='lime').generate(text)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig('wordcloud.png')
plt.show()
