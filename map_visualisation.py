import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import PolyLineTextPath
from geopy.distance import geodesic

masters_with_lng_lat = pd.read_csv("masters_courses_with_coords" + ".csv")

def show_map(query_result):
    def add_coords(query_result):
    return query_result
    def beautify(query_result):
    def enum_it_to_txt(li):
        res = ""
        for i,line in enumerate(li):
            res += str(i+1) + ". " + line + "\n\\\\\\\\\\\n"
        return res

    essential_information = query_result.copy()
    essential_information.loc[:,"essential_description"] = essential_information.apply( lambda row: str(" - ".join(row[['courseName','fees']])) , axis=1 )
    # essential_information.loc[:,"essential_description"] = essential_information.apply( lambda row: str(" - ".join(row[['universityName','facultyName','courseName','fees']])) , axis=1 )
    essential_information = essential_information[["lng","lat","essential_description"]]
    essential_information = pd.DataFrame(essential_information.groupby(['lng','lat'])['essential_description'].apply(list).reset_index())
    essential_information["sharingSamePosition"] = essential_information.apply(lambda row : len(row["essential_description"]), axis=1)
    essential_information["essential_description"] = essential_information.apply(lambda row : enum_it_to_txt(row["essential_description"]), axis=1)
    return essential_information

    query_result = add_coords(query_result)
    query_result = beautify(query_result)




    gdf = gpd.GeoDataFrame(query_result, geometry=gpd.points_from_xy(query_result.lng, query_result.lat))

    # Create a Folium map centered at the mean location of the universities
    m = folium.Map(location=[query_result.loc[1,'lat'], query_result.loc[1,'lng']], zoom_start=7)

    # Add a marker for each university
    for index, row in gdf.iterrows():
    # print(index)
    # print(row)
    folium.Marker([row['lat'], row['lng']], popup=row['essential_description']).add_to(m)

    # Adding markers to the map and calculating distances
    for i in range(len(gdf)):
    for j in range(i+1, len(gdf)):
    # Drawing a polyline with text
        locations=[(gdf.loc[i, 'lat'], gdf.loc[i, 'lng']), (gdf.loc[j, 'lat'], gdf.loc[j, 'lng'])]
        # print(locations)
        distance = geodesic(locations[0], locations[1]).km
        folium.PolyLine(
            locations=locations,
            color='red',
            weight=1,
            opacity=0.5
        ).add_to(m)

        # PolyLineTextPath(
        #    m,
        #    locations=locations,
        #    color='blue',
        #    text='hello',
        #    repeat=True,
        #    offset=5,
        #    font_size=15,
        #    font_color='black',
        #    arrow_color='black',
        #    arrow_size=15,
        #    arrow_frequency=1000
        # ).add_to(m)


        # break
    # break
