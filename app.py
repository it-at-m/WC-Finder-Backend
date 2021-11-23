# for deployment
# gcloud builds submit --tag gcr.io/lhm-14-dps/toilets
# gcloud run deploy --image gcr.io/lhm-14-dps/toilets --platform managed

from flask import Flask, request, Response, send_file
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

@app.route('/get_image/<path:image_path>')
def get_image(image_path):
    return send_file(image_path)

@app.route('/get_layout/<path:plan_path>')
def get_layout(plan_path):
    return send_file(plan_path)

@app.route('/filter/', methods=["GET", "POST"])
def filtering():
    data = request.get_json()
    model.filter_ramp(data["Ramp"]) # keep it first filter for now
    model.filter_door(data["DoorWidth"])
    model.filter_key(data["EuroKey"])
    filtered_toilets = model.nearby_df.to_json(orient="records")
    return filtered_toilets

    # if "Ramp" in data.keys():
    #     model.filter_ramp(data["Ramp"]) # keep it first filter for now
    # else:
    #     model.filter_ramp(0)
    # if "DoorWidth" in data.keys():
    #     model.filter_door(data["DoorWidth"])
    # else:
    #     model.filter_door(0)
    # if "EuroKey" in data.keys():
    #     model.filter_door(data["EuroKey"])
    # else:
    #     model.filter_key(1)
    #
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
    
