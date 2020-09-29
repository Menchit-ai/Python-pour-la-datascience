import pandas as pd
import numpy as np


#function to convert to alpha2 country codes and continents
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
def get_continent(col):
    try:
        cn_a2_code =  country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown' 
    try:
        cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    except:
        cn_continent = 'Unknown' 
    return (cn_a2_code, cn_continent)

#function to get longitude and latitude data from country name
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent = "appli")
def geolocate(country):
    try:
        # Geolocate the center of the country
        loc = geolocator.geocode(country)
        # And return latitude and longitude
        return (loc.latitude, loc.longitude)
    except:
        # Return missing value
        return np.nan




data = pd.read_csv("abo.csv",delimiter=',')
coord = pd.read_csv("world_coord.csv",delimiter=',', encoding='latin1')
country = data["Pays"]
data_abo = data[data["VAR"] == "BB-P100-TOT"]
data_abo = data_abo[data_abo["TIME"] == "2019"]

test = data_abo["Value"]

print(country.unique())
print(coord["Country"])
print(data_abo)

print(str(coord["Country"][0]))
print(data_abo.iloc[0]["Value"])

#Create a world map to show distributions of users 
import folium
from folium.plugins import MarkerCluster
#empty map
world_map= folium.Map(tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(world_map)
#for each coordinate, create circlemarker of user percent
for i in range(len(data_abo)):
    for k in range(len(coord)):
        if(str(coord["Country"][k]) == str(data_abo["Pays"].unique()[i])):
            lat = coord['latitude'][k]
            longit = coord['longitude'][k]

    radius=5
    popup_text = """Country : {}<br>
                %of Users : {}<br>"""
    popup_text = popup_text.format(data_abo.iloc[i]["Pays"],
                            data_abo.iloc[i]["Value"]
                            )
    folium.CircleMarker(location = [lat, longit], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
#show the map
world_map.save(outfile='map.html')