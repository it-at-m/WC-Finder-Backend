from flask import Flask, request, jsonify
import folium
from inference import LHMModel

app = Flask(__name__)

model = None

@app.before_first_request
def load_model():
    global model
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
    model.nearby_toilets(data["distance"])
    return model.map_nearby_toilets()

# @app.route('/mapped')
# def mapped_toilets():
#     global model
#     mapped = model.map_nearby_toilets()
#     return mapped

if __name__ == '__main__':
    app.run(debug=True)
