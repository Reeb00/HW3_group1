import pandas as pd
import requests
import json
from time import sleep
import os
import general_functions


def get_coordinates(uni):
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

def get_all_coords(universityNames):
    latlist = []
    lnglist = []
    for uniName in universityNames:
        sleep(0.1)
        lat, lng = get_coordinates(uniName)
        latlist.append(lat)
        lnglist.append(lng)
    return pd.DataFrame({'universityName':universityNames, 'lat':latlist, 'lng':lnglist})

def load_coords():
    file_path = "uni_coords.csv"
    if not(os.path.isfile(file_path)):
        universityNames = general_functions.get_dataset()['universityName'].drop_duplicates().tolist()
        uni_coords = get_all_coords(universityNames)
        uni_coords.to_csv("uni_coords.csv", index=False)
    return pd.read_csv("uni_coords.csv", usecols=['universityName','lat','lng'])

def add_coords(query_result):
    uni_coords = load_coords()
    query_result = pd.merge(query_result, uni_coords, how='left', left_on=['universityName'], right_on=['universityName'])
    # query_result = pd.merge(query_result, city_coords, how='left', left_on=['country','city'], right_on=['country','city'])
    return query_result


