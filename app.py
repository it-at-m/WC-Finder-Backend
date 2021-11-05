from flask import Flask, request, jsonify
import folium
from inference import LHMModel

app = Flask(__name__)

model = LHMModel()


@app.route('/')
def show_center():
    center = model.show_center()
    return center

@app.route('/address', methods=['POST', "GET"])
def get_address():
    global model
    model = LHMModel()
    data = request.get_json()
    model.geo_from_address(data["address"])
    return model.nearby_toilets(data["distance"])


# @app.route('/mapped')
# def mapped_toilets():
#     mapped = model.map_nearby_toilets()
#     return mapped

if __name__ == '__main__':
    app.run(debug=True)