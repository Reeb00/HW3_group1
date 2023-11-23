import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import PolyLineTextPath
from geopy.distance import geodesic

masters_with_lng_lat = pd.read_csv("masters_courses_with_coords" + ".csv")

def enum_list_to_txt(li):
    if len(li)==1:
        return li[0]
    else:
        res = ""
        for i,line in enumerate(li):
            res += str(i+1) + ". " + line + "\n\\\\\\\\\\\n"
        return res

def beautify(query_result):
    essential_information = query_result.copy()
    essential_information.loc[:,"essential_description"] = essential_information.apply( lambda row: str(" - ".join(row[['courseName','fees']])) , axis=1 )
    # essential_information.loc[:,"essential_description"] = essential_information.apply( lambda row: str(" - ".join(row[['universityName','facultyName','courseName','fees']])) , axis=1 )
    essential_information = essential_information[["lng","lat","essential_description",'country','city','universityName']]
    essential_information = pd.DataFrame(essential_information.groupby(['lng','lat','country','city','universityName'])['essential_description'].apply(list).reset_index())
    essential_information["sharingSamePosition"] = essential_information.apply(lambda row : len(row["essential_description"]), axis=1)
    essential_information["essential_description"] = essential_information.apply(lambda row : enum_list_to_txt(row["essential_description"]), axis=1)
    return essential_information


def show_map(query_result):
    gdf = gpd.GeoDataFrame(query_result, geometry=gpd.points_from_xy(query_result.lng, query_result.lat))

    # create map
    m = folium.Map()

    # Add a marker for each university
    for i, row in gdf.iterrows():
        folium.Marker([row['lat'], row['lng']], popup=row['essential_description']).add_to(m)

    # Adding markers to the map and calculating distances
    for i in range(len(gdf)):
        for j in range(i+1, len(gdf)):
        # Drawing a polyline with text
            locations=[(gdf.loc[i, 'lat'], gdf.loc[i, 'lng']), (gdf.loc[j, 'lat'], gdf.loc[j, 'lng'])]
            distance = geodesic(locations[0], locations[1]).km
            folium.PolyLine(
                locations=locations,
                color='red',
                weight=3,
                opacity=0.5,
                tooltip=gdf.loc[i,'universityName'] + " - " + gdf.loc[j,'universityName'] + "\n(distance: " + "{:.2f}".format(distance) + " km)",
                # popup=str(distance) + " km",
            ).add_to(m)
        
    # fitting the zoom-factor
    southwest_corner = query_result[['lat', 'lng']].min().tolist()
    northeast_corner = query_result[['lat', 'lng']].max().tolist()
    m.fit_bounds([southwest_corner, northeast_corner]) 
    return m