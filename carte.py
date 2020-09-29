import pandas as pd
import numpy as np

from googletrans import Translator

import pycountry

#function to translate French coutry name to English name
def translate_to_english(word):
    translator = Translator()
    try:
        res = translator.translate(word)
        res = res.text
    except:
        res = None
    return res

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
country = data["Pays"]

input_countries = country.unique()
li = []
for i in input_countries:
    li.append(translate_to_english(i))

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2

codes = [countries.get(country, 'Unknown code') for country in li]

print(codes)  # prints ['AS', 'CA', 'FR']
quit()

ad = len(country)
for i in range(len(country)):
    data["EnglishCountry"] = translate_to_english(country[i])
    print(i/ad)

print(data.head(40))








# # Create a world map to show distributions of users 
# import folium
# from folium.plugins import MarkerCluster
# #empty map
# world_map= folium.Map(tiles="cartodbpositron")
# marker_cluster = MarkerCluster().add_to(world_map)
# #for each coordinate, create circlemarker of user percent
# for i in range(len(df)):
#         lat = df.iloc[i]['Latitude']
#         longit = df.iloc[i]['Longitude']
#         radius=5
#         popup_text = """Country : {}<br>
#                     %of Users : {}<br>"""
#         popup_text = popup_text.format(df.iloc[i]['Country'],
#                                    df.iloc[i]['User_Percent']
#                                    )
#         folium.CircleMarker(location = [lat, longit], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
# #show the map
# world_map