from flask import Flask, request, Response
from flask_restful import Resource, Api
from inference import LHMModel
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = None

@app.before_first_request
def load_model():
    global model
    model = LHMModel()

@app.route('/')
def show_all():
    all_toilets = model.show_all()
    return all_toilets


# @app.route('/address', methods=["GET", "POST"])
# def get_address():
#     global model
#     data = request.get_json()
#
#     if ("address" not in data.keys()) or (data["address"] is None):
#         input_address = "Freddie-Mercury-Str. 5"
#     else:
#         input_address = data["address"]
#
#     if ("distance" not in data.keys()) or (data["distance"] is None):
#         input_distance = 1000
#     else:
#         input_distance = data["distance"]
#
#     model.geo_from_address(input_address)
#     toilets = model.nearby_toilets(input_distance)
#     return toilets

# @app.route('/mapped')
# def mapped_toilets():
#     mapped = model.map_nearby_toilets()
#     return mapped


if __name__ == '__main__':
    app.run(debug=True)
    
