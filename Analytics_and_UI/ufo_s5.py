import pandas as pd
import couchdb
import folium
import seaborn as sns
from datetime import datetime as dt
import matplotlib.pyplot as plt
from folium.plugins import HeatMap
import requests
import overpy

#Connecting to CouchDB server
couch = couchdb.Server('http://admin:admin@172.26.134.93:5984/')

#Choosing Our DB
db = couch['twitter-final']
view_name = '_design/aliens/_view/aliens_og'
view = db.view(view_name)

author_id_list = []
sentiment_list = []
text_list = []
created_at_list = []
bbox_list = []
full_name_list = []

#Pulling our Information
for row in view:
    data = row.value.get('data')
    includes = row.value.get('includes')

    # Extracting the individual parameters from data
    author_id = data.get('author_id')
    sentiment = data.get('sentiment')
    text = data.get('text')
    created_at = data.get('created_at')

    # Extracting the individual parameters from includes
    places = includes.get('places')
    if places:
        bbox = places[0].get('geo', {}).get('bbox')
        full_name = places[0].get('full_name')
    else:
        bbox = None
        full_name = None

    author_id_list.append(author_id)
    sentiment_list.append(sentiment)
    text_list.append(text)
    created_at_list.append(created_at)
    bbox_list.append(bbox)
    full_name_list.append(full_name)

#Creating a DF
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


#Australia Map
map_australia = folium.Map(location=[-25, 135], zoom_start=4, tiles='cartodbpositron')

#Add alien-themed map tiles
#folium.TileLayer('http://alienmaps.arc.nasa.gov/images/cea/{z}/{x}/{y}.png', attr='Alien Maps').add_to(map_australia)

#Initializing Overpass API
api = overpy.Overpass()

#Defining the bounding boxes for Australia
bounding_boxes = [
    (112.9, -44.1, 154.1, -10.7),   # Western Australia
    (129.0, -44.1, 153.6, -10.7),   # Northern Territory
    (112.9, -39.2, 154.1, -28.2),   # South Australia
    (141.0, -39.2, 154.1, -28.2),   # Victoria
    (141.0, -39.2, 153.6, -28.2),   # New South Wales
    (141.0, -28.9, 153.6, -10.7),   # Queensland
    (113.9, -28.9, 129.0, -26.7)    # Australian Capital Territory and Tasmania
]

#retrieving 800 locations to not clutter the map too much
max_locations = 800

locations = []
for bbox in bounding_boxes:
    query = f"""
        node["amenity"="fast_food"]["name"~"McDonald's", i]({bbox[1]}, {bbox[0]}, {bbox[3]}, {bbox[2]});
        out center;
    """
    result = api.query(query)
    locations.extend(result.nodes)

    if len(locations) >= max_locations:
        break

locations = locations[:max_locations]

heat_data = [[node.lat, node.lon] for node in df.itertuples()]

# Creating Heatmap
HeatMap(heat_data, name='Tweet Count Heatmap').add_to(map_australia)

for node in locations:
    lat = node.lat
    lon = node.lon
    name = node.tags.get("name", "McDonald's")
    folium.Marker(location=[lat, lon], popup=name, icon=folium.Icon(icon='alien')).add_to(map_australia)

#Adding layer control to the map
folium.LayerControl().add_to(map_australia)

#Displaying the map
map_australia.save('mcdonalds_map.html')
