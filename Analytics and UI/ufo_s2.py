#births deaths

import pandas as pd
import couchdb
import matplotlib.pyplot as plt

#Connecting to our couch DB Server
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
    created_at = pd.to_datetime(data.get('created_at'))  # Convert to datetime type

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

# Split full_name to extract state name
df['state_name'] = df['full_name'].str.split(',').str[-1].str.strip()

import pandas as pd
import folium

# Read the dataset
data = pd.read_csv('births_and_deaths.csv')

# Filter the DataFrame to include only the relevant columns
births_deaths_df = data[['state_name_2016', 'births_2020_21', 'deaths_2020_21']].copy()

# Calculate the births to deaths ratio
births_deaths_df['births_to_deaths_ratio'] = births_deaths_df['births_2020_21'] / births_deaths_df['deaths_2020_21']

# Group the data by state and calculate the sum of births and deaths
statewise_data = births_deaths_df.groupby('state_name_2016').sum().reset_index()

# Create a dictionary of state coordinates
state_coordinates = {
    'Queensland': (-20.9176, 142.7028),
    'New South Wales': (-33.8688, 151.2093),
    'Victoria': (-37.8136, 144.9631),
    'South Australia': (-34.9285, 138.6007),
    'Western Australia': (-31.9505, 115.8605),
    'Tasmania': (-42.8821, 147.3272),
    'Northern Territory': (-12.4634, 130.8456),
    'Australian Capital Territory': (-35.2809, 149.1300)  # Add coordinates for the Australian Capital Territory
}

# Create a Folium Map centered on Australia
map_center = [-25, 135]
map_statewise = folium.Map(location=map_center, zoom_start=4)

# Iterate over the statewise data and add circles to the map
for index, row in statewise_data.iterrows():
    state_name = row['state_name_2016']
    births_deaths_ratio = row['births_to_deaths_ratio']

    # Set the circle color based on births to deaths ratio
    if births_deaths_ratio >= 1:
        circle_color = 'green'
    else:
        circle_color = 'red'

    # Get the coordinates for the state
    state_location = state_coordinates[state_name]

    # Create a circle with the specified color and radius based on the consolidated values
    circle = folium.Circle(
        location=state_location,
        radius=100000,  # Adjust the radius as needed
        color=circle_color,
        fill=True,
        fill_color=circle_color
    )

    # Add a tooltip with the state name and births to deaths ratio
    tooltip = f"State: {state_name}<br>Births to Deaths Ratio: {births_deaths_ratio:.2f}"
    circle.add_child(folium.Tooltip(tooltip))

    # Add the circle to the map
    circle.add_to(map_statewise)

    # Filter the tweets based on the state name
    state_tweets = df[df['state_name'] == state_name]

    # Count the tweets for the state
    tweet_count = len(state_tweets)

    # Add the count of tweets as text on each state
    folium.Marker(
        location=state_location,
        icon=folium.DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html=f"<div style='font-size: 12pt;'>Tweet Count: {tweet_count}</div>"
        )
    ).add_to(map_statewise)



# Save the map as an HTML file
map_statewise.save('statewise_births_deaths_map.html')

print(df.info())
