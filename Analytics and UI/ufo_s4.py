#Milk Production

import pandas as pd
import couchdb
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from folium.plugins import HeatMap

# Set Seaborn and Matplotlib style to 'ticks' with a pleasing color palette
sns.set_style('ticks')
sns.set_palette('PuBuGn_d')

# Connect to CouchDB server
couch = couchdb.Server('http://admin:admin@172.26.134.93:5984/')

# Select the desired database
db = couch['twitter-final']

# Define the name of the view
view_name = '_design/aliens/_view/aliens_og'

# Retrieve the view
view = db.view(view_name)

# Initialize empty lists to store the extracted values
author_id_list = []
sentiment_list = []
text_list = []
created_at_list = []
bbox_list = []
full_name_list = []

# Iterate over the rows of the view and extract the values
for row in view:
    data = row.value.get('data')
    includes = row.value.get('includes')

    # Extract the individual parameters from 'data'
    author_id = data.get('author_id')
    sentiment = data.get('sentiment')
    text = data.get('text')
    created_at = data.get('created_at')

    # Extract the individual parameters from 'includes'
    places = includes.get('places')
    if places:
        bbox = places[0].get('geo', {}).get('bbox')
        full_name = places[0].get('full_name')
    else:
        bbox = None
        full_name = None

    # Append the extracted values to the respective lists
    author_id_list.append(author_id)
    sentiment_list.append(sentiment)
    text_list.append(text)
    created_at_list.append(created_at)
    bbox_list.append(bbox)
    full_name_list.append(full_name)

# Create a DataFrame using the extracted values
data = {
    'author_id': author_id_list,
    'sentiment': sentiment_list,
    'text': text_list,
    'created_at': created_at_list,
    'bbox': bbox_list,
    'full_name': full_name_list
}
df = pd.DataFrame(data)

def convert_bbox_to_lat_long(bbox):
    if len(bbox) == 4:
        lat = (bbox[1] + bbox[3]) / 2
        lon = (bbox[0] + bbox[2]) / 2
        return lat, lon
    else:
        return None, None

df['lat'], df['lon'] = zip(*df['bbox'].map(convert_bbox_to_lat_long))
df = df.dropna(subset=['lat', 'lon'])

print(df.info())

# Existing code for milk production graph
states = ['Victoria', 'New South Wales', 'Tasmania', 'South Australia', 'Western Australia', 'Queensland']
milk_production = [
    [411.90, 471.60, 564.70, 623.10, 586.40, 541.30, 445.20, 347.80, 354.20, 357.50, 389.30, 371.90],
    [92.30, 98.40, 100.20, 105, 99.50, 96.70, 91, 79.80, 80.70, 74.40, 76.70, 77.80],
    [22.30, 36.50, 83, 112.60, 113.50, 108, 92.50, 75.10, 77, 69.90, 60.20, 36.40],
    [34, 36.30, 45.60, 50.80, 49.70, 45.40, 40.60, 36.60, 40.90, 38.90, 38.30, 33.20],
    [29.10, 29, 30.90, 32.60, 30.70, 28.70, 26.20, 23.90, 26.80, 26, 28, 28.60],
    [26, 27.70, 28.40, 28.80, 27.70, 26.70, 24.90, 22.30, 21.50, 21.40, 21.80, 22]
]

# Plot the milk production graph
fig, ax1 = plt.subplots(figsize=(10, 6))
for i, state in enumerate(states):
    ax1.bar(state, milk_production[i], label='Milk Production')

ax1.set_xlabel('State')
ax1.set_ylabel('Milk Production (in millions)')
ax1.set_title('Milk Production and Tweet Count by State')

# Load tweet data and calculate tweet count by state

# Extract state names from 'full_name' column
df['state'] = df['full_name'].str.split(',').str[-1].str.strip().str.lower()

state_tweet_count = df['state'].value_counts()

# Create secondary y-axis for tweet count
ax2 = ax1.twinx()

# Plot the tweet count on top of the existing graph
tweet_counts = []
for i, state in enumerate(states):
    state_lower = state.lower()  # Convert state name to lowercase for comparison
    if state_lower in state_tweet_count:
        tweet_count = state_tweet_count[state_lower]
    else:
        tweet_count = 0
    tweet_counts.append(tweet_count)

ax2.bar(states, tweet_counts, alpha=0.2, color='lime', label='Tweet Count')
ax2.set_ylabel('Tweet Count')

# Adjust the scale of the secondary y-axis
ax2.set_ylim(0, max(tweet_counts) + 100)

# Display legend
#ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Add data labels to the bars
for i, state in enumerate(states):
    ax1.text(state, milk_production[i][-1] + 20, str(int(milk_production[i][-1])), ha='center', fontsize=8)
    ax2.text(state, tweet_counts[i] + 20, str(tweet_counts[i]), ha='center', fontsize=8)

# Customize the appearance of the plot
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.grid(True)

# Adjust the layout
plt.tight_layout()

# Create a folium map centered around Australia
map_center = [-25, 134]
milk_map = folium.Map(location=map_center, zoom_start=4)

# Define colors for the sentiment heat map
sentiment_colors = ['purple', 'lime', 'orange']  # Low sentiment to high sentiment

# Create a feature group for the circle markers
circle_markers = folium.FeatureGroup(name='Circle Markers')

# Add circles representing production volume
max_volume = np.max(milk_production)
scale_factor = 1  # Scale factor for circle radius

for i, state in enumerate(states):
    state_lower = state.lower()  # Convert state name to lowercase for comparison

    if state_lower in df['state'].values:
        state_data = df[df['state'] == state_lower]
        lat, lon = state_data['lat'].values[0], state_data['lon'].values[0]

        volume = milk_production[i][-1]  # Get the latest month's production volume
        radius = np.sqrt(volume) * scale_factor

        # Create the circle marker
        circle_marker = folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color='white',
            fill_color='white',
            fill_opacity=0.5
        )
        circle_marker.add_to(circle_markers)

# Add the circle markers feature group to the map
circle_markers.add_to(milk_map)

# Create a feature group for the heatmap layer
heatmap_layer = folium.FeatureGroup(name='Heatmap Layer')

# Add sentiment heat map layer
heat_data = df[['lat', 'lon', 'sentiment']]
heat_data = heat_data.dropna()  # Drop rows with missing latitude or longitude
heat_array = heat_data.values
heatmap = folium.plugins.HeatMap(heat_array, radius=15, gradient={0.2: sentiment_colors[0], 0.5: sentiment_colors[1], 0.8: sentiment_colors[2]})
heatmap.add_to(heatmap_layer)

# Add the heatmap layer feature group to the map
heatmap_layer.add_to(milk_map)

# Add layer control to switch between different map views
folium.LayerControl().add_to(milk_map)

# Save the map to an HTML file
milk_map.save('milk_production_map.html')
