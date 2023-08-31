import base64
from flask import Flask, request, jsonify, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import time
import random
import string

uri = "mongodb+srv://Brain3DVizMember:<password>@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
#select the specific database and the collection
db = client["Reaction-Time"]
responses_collection = db["responses"]

app = Flask(__name__)
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
    with open("Dataset/Images/image{index}.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    with open("Dataset/Labels/annotations{index}.txt", 'r') as file:
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
    

@app.route('/get-info-form', methods=['GET'])
def get_info_form():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({"message": "Session expired or not started."})
    
    index = session.get('index', 0)
    # Other processing...
    return jsonify({"formItems": sample_form_items, "user_id": user_id, "index": index})

@app.route('/game/begin', methods=['GET'])
def game_begin():
    user_id = generate_unique_user_id()  # Generate a unique user ID
    session['user_id'] = user_id
    session['index'] = 0
    # Other processing...
    next_image = get_data(session["index"])
    return jsonify(next_image)

@app.route('/game/next', methods=['POST'])
def game_next():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({"message": "Session expired or not started."})

    data = request.json
    time = data.get('time')
    num_of_errors = data.get('numOfErrors')
    user_info = data.get('userInfo')
    
    # Store response data in MongoDB
    response_data = {
        "user_id": user_id,
        "index": session['index'],
        "time": time,
        "numOfErrors": num_of_errors,
        "userInfo": user_info
    }
    responses_collection.insert_one(response_data)

    # Update index
    session['index'] += 1
    
    next_image = get_data(session["index"])

    return jsonify(next_image)

if __name__ == '__main__':
    app.run(debug=True)