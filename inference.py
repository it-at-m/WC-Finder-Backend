from typing import Optional
import json
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from geopy.geocoders import GoogleV3
from pyproj import Geod
from shapely.geometry import Point, LineString

class LHMModel:

    def __init__(self):
        self.df = pd.read_json('toilets.json')
        self.current = None
        self.nearby_df = None
        self.nearby_json = None

    def show_center(self):
        boulder_coords = [48.8584, 2.2945]
        my_map = folium.Map(location=boulder_coords, zoom_start=13)

        return my_map._repr_html_()

    def geo_from_address(self, street_hn, city="Munich", country="Germany"):
        locator = GoogleV3(api_key="AIzaSyBAu96ruSZwSGt8t8muUYlvGLmiHmSSeJQ")
        location = locator.geocode(street_hn + ", " + city + ", " + country)
        self.current = (location.latitude, location.longitude)


    def nearby_toilets(self, distance):
        geod = Geod(ellps="WGS84")
        self.nearby_df = self.df[self.df['geometry'].map(lambda x: geod.geometry_length(LineString([Point(x), self.current]))) < distance]
        self.nearby_df = self.nearby_df.rename(columns={"geometry":"position"})
        self.nearby_df = self.nearby_df[['title', 'short_description', 'position']]
        result = self.nearby_df.to_json(orient="records")
        return result

    # def map_nearby_toilets(self):
    #     my_map = folium.Map(location=self.current, zoom_start=15)
    #     folium.Marker(location=self.current, icon=folium.Icon(
    #                               icon_color='green', #acceptable colors are thos in color_options set.
    #                               prefix='glyphicon')).add_to(my_map)
    #     for index, location_info in self.nearby_df.iterrows():
    #         folium.Marker(location=(location_info['latitude'], location_info["longitude"]), popup=location_info["title"]).add_to(my_map)
    #
    #     return my_map._repr_html_()

    def filter_further(self):
        pass
