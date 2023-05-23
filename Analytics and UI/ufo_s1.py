import pandas as pd
import couchdb
import matplotlib.pyplot as plt
import os

if not os.path.exists('static/images'):
    os.makedirs('static/images')

#Alien Theme :)
plt.style.use('dark_background')

# Connect to CouchDB server
couch = couchdb.Server('http://admin:admin@172.26.134.93:5984/')

#DB Name
db = couch['twitter-final']

# View Name
view_name = '_design/aliens/_view/aliens_og'
view = db.view(view_name)

# Initialize empty lists to store the extracted values
author_id_list = []
sentiment_list = []
text_list = []
created_at_list = []
bbox_list = []
full_name_list = []

for row in view:
    data = row.value.get('data')
    includes = row.value.get('includes')

    # Extracting individual parameters from data
    author_id = data.get('author_id')
    sentiment = data.get('sentiment')
    text = data.get('text')
    created_at = data.get('created_at')

    # Extracting individual parameters from includes
    places = includes.get('places')
    if places:
        bbox = places[0].get('geo', {}).get('bbox')
        full_name = places[0].get('full_name')
    else:
        bbox = None
        full_name = None

    # Appending extracted values to the respective lists
    author_id_list.append(author_id)
    sentiment_list.append(sentiment)
    text_list.append(text)
    created_at_list.append(created_at)
    bbox_list.append(bbox)
    full_name_list.append(full_name)

#making a DF
data = {
    'author_id': author_id_list,
    'sentiment': sentiment_list,
    'text': text_list,
    'created_at': created_at_list,
    'bbox': bbox_list,
    'full_name': full_name_list
}
df = pd.DataFrame(data)

btc_df = pd.read_csv("BTC-USD.csv")

#converting to DateTime format
btc_df["Date"] = pd.to_datetime(btc_df["Date"])

btc_df.set_index("Date", inplace=True)

#grouping by Week
df["created_at"] = pd.to_datetime(df["created_at"])
df.set_index("created_at", inplace=True)
tweet_count = df.resample('W').size()

# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot the BTC closing price
ax1.plot(btc_df.index, btc_df["Close"], color="cyan", label="BTC Closing Price")
ax1.set_xlabel("Date")
ax1.set_ylabel("BTC Closing Price")
ax1.tick_params(axis="y", labelcolor="cyan")

# Create a secondary axis for the tweet count
ax2 = ax1.twinx()
ax2.plot(tweet_count.index, tweet_count.values, color="lime", label="Tweet Count")
ax2.set_ylabel("Tweet Count")
ax2.tick_params(axis="y", labelcolor="lime")

plt.title("BTC Closing Price and Tweet Count over Time (Weekly)")
lines = ax1.get_lines() + ax2.get_lines()
labels = [line.get_label() for line in lines]
plt.legend(lines, labels)

plt.tight_layout()
plt.savefig('static/images/scenario1.png')  # Save the plot to a file
plt.show()
