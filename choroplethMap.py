import folium
import json
import pandas as pd 
import numpy as np
import geopandas as gpd

# world map from https://github.com/johan/world.geo.json/blob/master/countries.geo.json with all countries activated

world_json_path = './world.json'
world_json = json.load(open(world_json_path))
print(world_json.keys())


gdf = gpd.read_file(world_json_path)
print(gdf.head())

data = pd.read_csv('./data_world/happiness-cantril-ladder.csv')
data = data[data['Year']==2012]

# Initialize the map:
m = folium.Map(location=[37, -102], zoom_start=5)
 
# Add the color for the chloropleth:
cho = folium.Choropleth(
 geo_data=world_json,
 name='choropleth',
 data=data,
 columns=['Code', 'Life satisfaction in Cantril Ladder (World Happiness Report 2019)'],
 key_on='feature.id',
 fill_color='GnBu',
 fill_opacity=0.7,
 line_opacity=0.2,
 legend_name='Life satisfaction in Cantril Ladder (World Happiness Report 2019)',
 bins=[0,2,3,4,5,6,7,8,9,10]
).add_to(m)

style_function = "font-size: 15px; font-weight: bold"
cho.geojson.add_child(
    folium.features.GeoJsonTooltip(['name'], style=style_function, labels=False))

folium.LayerControl().add_to(m)


m.save('test.html')