import base64, os
from flask import Flask, render_template, request, jsonify, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_session import Session
import uuid
import time
import random
import string

# uri = "mongodb+srv://Brain3DVizMember:<password>@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment.`` You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
# #select the specific database and the collection
# db = client["Reaction-Time"]
# responses_collection = db["responses"]

app = Flask(__name__, static_url_path = '/static')
# Configure the app to use sessions
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
#app.secret_key = 'your_secret_key'

# CONST variables
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400

#generate unique user id
def generate_unique_user_id():
    timestamp = str(int(time.time() * 1000))  # Current timestamp in milliseconds
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    unique_id = f"{timestamp}_{random_chars}"
    return unique_id

# get image and annotation data
def get_data(index):
    with open("./static/Images/image{}.png".format(index), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    with open("./static/Labels/image{}.txt".format(index), 'r') as file:
        line = file.read().split()
        x_center = float(line[1]) * IMAGE_WIDTH
        y_center = float(line[2]) * IMAGE_HEIGHT
        width = float(line[3]) * IMAGE_WIDTH
        height = float(line[4]) * IMAGE_HEIGHT
    data = {
        "image": encoded_string,
        "posY": y_center,
        "posX": x_center,
        "width": width,
        "height": height
    }
    return data

@app.route('/')
def index():
    # Store data in MongoDB
    # Store session index and user ID
    #session['index'] = 100 #generate_unique_user_id()  # Replace with your session index value
    # session['user_id'] = 0  # Replace with your user ID value
    return render_template('index.html')

@app.route('/get-info-form', methods=['GET'])
def get_info_form():
    # Store response data in MongoDB
    response_data = {
        "formItems": [
            {"value": "Full Name", "type": "string"},
            {"value": "Age", "type": "number"},
            {"value": "School", "type": "string"},
            {"value": "Sex", "type": "select", "options": ["Male", "Female", "Prefer not to say"]}
        ]
    }

    return jsonify(response_data)

@app.route('/save-form-data', methods=['POST'])
def save_form_data():
    # Other processing...
    data = request.json
    age = data.get('Age')
    sex = data.get('Sex')
    school = data.get('School')
    full_name = data.get('Full Name')

    # Store response data in MongoDB
    # response_data = {
    #     "user_id": session['user_id'],
    #     "age": age,
    #     "sex": sex,
    #     "full_name": full_name
    # }
    #responses_collection.insert_one(response_data)
    response_data = {
        "user_id": generate_unique_user_id()
    }

    return jsonify(response_data)

@app.route('/game-begin', methods=['GET'])
def game_begin():
    # Other processing...session["index"]
    next_image = get_data(0)

    next_image["max_images"] = 25 # CHANGE AS NEEDED
    next_image["target"] = "Find the Red Square" # CHANGE AS NEEDED
    next_image["find_position"] = True

    return jsonify(next_image)

@app.route('/game-next', methods=['POST'])
def game_next():
    # user_id = session.get('user_id')
    # if user_id is None:
    #     return jsonify({"message": "Session expired or not started."})

    data = request.json
    time = data.get('time')
    num_of_errors = data.get('numOfErrors')
    user_ID = data.get('user-ID')
    user_index = data.get('user-index')
    
    # Store response data in MongoDB
    # response_data = {
    #     "index": session['index'],
    #     "time": time,
    #     "numOfErrors": num_of_errors,
    #     "user-ID": user_ID,
    #     "user-index": user_index
    # }
    ### Add "target": "Blue Triangle" to give indicator ###

    #responses_collection.insert_one(response_data)

    # Update index
    # user_index += 1

    next_image = get_data(user_index)

    if user_index == 11:
        next_image["target"] = "Is a Red Square Present?"  # CHANGE AS NEEDED
    if user_index > 10:
        next_image["find_position"] = False
        next_image["present"] = True
    else:
        next_image["find_position"] = True

    return jsonify(next_image)

if __name__ == '__main__':
    app.run(debug=True)
