# for deployment
# gcloud builds submit --tag gcr.io/lhm-14-dps/toilets
# gcloud run deploy --image gcr.io/lhm-14-dps/toilets --platform managed

from flask import Flask, request, send_file
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
    model.filter_ramp(data["Ramp"])  # keep it first filter for now
    model.filter_door(data["DoorWidth"])
    model.filter_key(data["EuroKey"])
    filtered_toilets = model.nearby_df.to_json(orient="records")
    return filtered_toilets


if __name__ == '__main__':
    app.run(debug=True)
    
