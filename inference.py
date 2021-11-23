import folium
import pandas as pd
from geopy.geocoders import GoogleV3
from pyproj import Geod
from shapely.geometry import Point, LineString
from flask_restful import Resource, Api

class LHMModel(Resource):

    def __init__(self):
        self.df = pd.read_json('./preprocessing/toilets_v6.json')
        # self.current = None
        self.nearby_df = None

    def show_all(self):
        all_toilets = self.df.to_json(orient="records")
        return all_toilets

    def filter_ramp(self, incline):
        self.nearby_df = self.df[self.df["ramp_steepness"] <= incline]

    def filter_door(self, width):
        self.nearby_df = self.nearby_df[self.nearby_df["door_width"] >= width]

    def filter_key(self, value):
        if value == 2:
            pass
        else:
            self.nearby_df = self.nearby_df[self.nearby_df["eurokey"] == value]

    # def geo_from_address(self, street_hn, city="Munich", country="Germany"):
    #     locator = GoogleV3(api_key="AIzaSyBAu96ruSZwSGt8t8muUYlvGLmiHmSSeJQ")
    #     location = locator.geocode(street_hn + ", " + city + ", " + country)
    #     self.current = (location.latitude, location.longitude)
    #
    # def nearby_toilets(self, distance):
    #     geod = Geod(ellps="WGS84")
    #     self.nearby_df = self.df[self.df['geometry'].map(lambda x: geod.geometry_length(LineString([Point(x), self.current]))) < distance]
    #     self.nearby_df = self.nearby_df.rename(columns={"geometry":"position"})
    #     self.nearby_df = self.nearby_df[['title', 'short_description', 'position']]
    #     result = self.nearby_df.to_json(orient="records")
    #     return result

    # def map_nearby_toilets(self):
    #     my_map = folium.Map(location=self.current, zoom_start=15)
    #     folium.Marker(location=self.current, icon=folium.Icon(
    #                               icon_color='green', #acceptable colors are thos in color_options set.
    #                               prefix='glyphicon')).add_to(my_map)
    #     for index, location_info in self.nearby_df.iterrows():
    #         folium.Marker(location=(location_info['latitude'], location_info["longitude"]), popup=location_info["title"]).add_to(my_map)
    #
    #     return my_map._repr_html_()

    # def filter_further(self):
    #     pass
