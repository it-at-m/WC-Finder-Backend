from flask import Flask, request, jsonify, Response
import folium
from inference import LHMModel
import json

app = Flask(__name__)

model = LHMModel()


@app.route('/')
def show_center():
    center = model.show_center()
    return center

@app.route('/address', methods=["GET"])
def get_address():
    global model
    model = LHMModel()
    if request.args.get("address") == None:
        input_address = "Freddie-Mercury-Str. 5"
    else:
        input_address =  request.args.get("address")

    if request.args.get("distance") == None:
        input_distance = 10000
    else:
        input_distance =  request.args.get("distance")
    model.geo_from_address(input_address)
    toilets = model.nearby_toilets(input_distance)
    res = Response(toilets, mimetype='text/json')
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res



# @app.route('/mapped')
# def mapped_toilets():
#     mapped = model.map_nearby_toilets()
#     return mapped

if __name__ == '__main__':
    app.run(debug=True)
