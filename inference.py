import pandas as pd


class LHMModel:

    def __init__(self):
        self.df = pd.read_json('./preprocessing/toilets_v14.json')
        self.df["modified"] = pd.to_datetime(self.df["modified"])
        self.df['modified'] = self.df['modified'].dt.strftime('%d-%m-%Y')
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

    def filter_grip(self, grips):
        self.nearby_df = self.nearby_df[self]
