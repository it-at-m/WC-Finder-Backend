from flask import Flask, request, Response
from inference import LHMModel

app = Flask(__name__)

model = LHMModel()


@app.route('/')
def show_center():
    center = model.show_center()
    return center

@app.route('/address', methods=["GET", "POST"])
def get_address():
    global model
    model = LHMModel()
    data = request.get_json()
    if ("address" not in data) or (data["address"] == None):
        input_address = "Freddie-Mercury-Str. 5"
    else:
        input_address =  data["address"]

    if ("distance" not in data) or (data["distance"] == None):
        input_distance = 1000
    else:
        input_distance =  data["distance"]
    model.geo_from_address(input_address)
    toilets = model.nearby_toilets(input_distance)
    print(input_address, input_distance)
    res = Response(toilets, mimetype='text/json')
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res



# @app.route('/mapped')
# def mapped_toilets():
#     mapped = model.map_nearby_toilets()
#     return mapped

if __name__ == '__main__':
    app.run(debug=True)
