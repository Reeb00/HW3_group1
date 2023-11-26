import pandas as pd
import requests
import json
from time import sleep
import os
import general_functions
from geopy.geocoders import Nominatim

# hardcoded coordinates
lat_lng_by_uni = {
    'University Centre of the West Fjords': (0,0),
}


def get_coordinates_by_uni(uni):
    if uni in lat_lng_by_uni:
        lat, lng = lat_lng_by_uni[uni]
        return lat, lng
    else:
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": uni,
            "format": "json"
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return None, None

def get_all_coords_by_uni(universityNames):
    latlist = []
    lnglist = []
    for uniName in universityNames:
        sleep(0.1)
        lat, lng = get_coordinates_by_uni(uniName)
        latlist.append(lat)
        lnglist.append(lng)
    return pd.DataFrame({'universityName':universityNames, 'lat':latlist, 'lng':lnglist})

def load_uni_coords():
    file_path = "uni_coords.csv"
    if not(os.path.isfile(file_path)):
        universityNames = general_functions.get_dataset()['universityName'].drop_duplicates().tolist()
        uni_coords = get_all_coords_by_uni(universityNames)
        uni_coords = uni_coords[~uni_coords.isnull().any(axis=1)] # removing rows with missing data
        uni_coords.to_csv("uni_coords.csv", index=False)
    return pd.read_csv(file_path, usecols=['universityName','lat','lng'])



def load_city_country_coords_where_necessary():
    file_path = "city_country_coords.csv"
    if not(os.path.isfile(file_path)):
        uni_coords = pd.read_csv("uni_coords.csv", usecols=['universityName'])['universityNames'].tolist()
        country_coords = general_functions.get_dataset()[['country', 'city','universityName']].drop_duplicates()
        country_coords = country_coords[~country_coords['universityName'].isin(uni_coords)]
        country_coords = country_coords[['country','city']].drop_duplicates()
        country_coords['lat_city'] = None
        country_coords['lng_city'] = None
        geolocator = Nominatim(user_agent="gettingCityCoords2")
        for index, row in country_coords.iterrows():
            location = geolocator.geocode(f"{row['city']}, {row['country']}")
            if location:
                lat, lng = location.latitude, location.longitude
                country_coords.loc[index,"lat_city"] = lat
                country_coords.loc[index,"lng_city"] = lng
        country_coords = country_coords[~country_coords.isnull().any(axis=1)] # removing rows with missing data
        country_coords.to_csv(file_path, index=False)
    return pd.read_csv(file_path)


def add_coords(query_result):
    uni_coords = load_uni_coords()
    query_result = pd.merge(query_result, uni_coords, how='left', left_on=['universityName'], right_on=['universityName'])
    country_coords = load_city_country_coords_where_necessary()
    query_result = pd.merge(query_result, country_coords, how='left', left_on=['country','city'], right_on=['country','city'])
    return query_result




