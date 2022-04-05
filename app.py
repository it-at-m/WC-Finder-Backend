from flask import Flask, request, Response, send_file, abort
from inference import LHMModel
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
from db_connection import get_connection, execute_sql

# contollers
from controllers.user_controller import *
from controllers.review_controller import *
from controllers.auth_controller import authorize


# load environment variables
load_dotenv()

# postgres connection object
pg = get_connection()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('FLASK_SECRET')
CORS(app, supports_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"

model = None


@app.before_first_request
def load_model():
    # if request.remote_addr not in ['127.0.0.1', '0.0.0.0', 'localhost', '192.168.254.3', '34.107.117.179']:
    #     abort(403)  # Forbidden
    global model
    model = LHMModel()


@app.route('/')
@cross_origin(supports_credentials=True)
# @authorize
def show_all():
    all_toilets = model.show_all()
    return all_toilets


@app.route('/get_image/<path:image_path>')
@cross_origin(supports_credentials=True)
# @authorize
def get_image(image_path):
    return send_file(image_path)


@app.route('/get_layout/<path:plan_path>')
@cross_origin(supports_credentials=True)
# @authorize
def get_layout(plan_path):
    return send_file(plan_path)


@app.route('/filter/', methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
# @authorize
def filtering():
    data = request.get_json()
    model.filter_ramp(data["Ramp"])  # keep it first filter for now
    model.filter_door(data["DoorWidth"])
    model.filter_key(data["EuroKey"])
    filtered_toilets = model.nearby_df.to_json(orient="records")
    return filtered_toilets

@app.route('/register', methods=['POST'])
def register():
    print("Inside register api")
    request_json = request.json
    payload = dict(
        email=request_json.get("email", None),
        first_name=request_json.get("first_name", None),
        last_name=request_json.get("last_name", None),
        password=request_json.get("password", None),
        confirm_password=request_json.get("confirm_password", None),
    )
    response = register_controller(payload=payload, db_conn=pg)
    return response

@app.route('/login', methods=['POST'])
def login():
    print("login api")
    request_json = request.json
    payload = dict(
        email=request_json.get("email", None),
        password=request_json.get("password", None),
    )
    response = login_controller(payload=payload, db_conn=pg)
    return response

@app.route('/review', methods=['POST'])
def review():
    print("review api")
    request_json = request.json
    accuracyDetails = [request_json.get("layouts", None),
                       request_json.get("filter", None),
                       request_json.get("direction", None),
                       request_json.get("euro", None)]
    payload = dict(
        toiletName=request_json.get("name", None),
        Experience=request_json.get("experience", None),
        CleanToilet=request_json.get("clean", None),
        LocateToilet=request_json.get("findToilet", None),
        Photo=request_json.get("photosUseful", None),
        Accuracy=request_json.get("infoAccurate", None),
        MoreInfo=request_json.get("moreExperience", None),
        accuracydetail = accuracyDetails
    )
    response = review_controller(payload=payload, db_conn=pg)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
