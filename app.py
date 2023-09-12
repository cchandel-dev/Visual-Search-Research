import base64, os, time, random, string
from flask import Flask, render_template, request, jsonify


app = Flask(__name__, static_url_path = '/static')
# Configure the app to use sessions
app.config['SESSION_TYPE'] = 'filesystem'

# CONST variables
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400

#generate unique user id
def generate_unique_user_id():
    timestamp = str(int(time.time() * 1000))  # Current timestamp in milliseconds
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    unique_id = f"{timestamp}_{random_chars}"
    return unique_id

# get image and annotation object detection data
def get_object_detection_data(index):
    with open("./static/object-detection/Images/image{}.png".format(index), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    with open("./static/object-detection/Labels/image{}.txt".format(index), 'r') as file:
        line = file.read().split()
        x_center = float(line[1]) * IMAGE_WIDTH
        y_center = float(line[2]) * IMAGE_HEIGHT
        width = float(line[3]) * IMAGE_WIDTH
        height = float(line[4]) * IMAGE_HEIGHT
    data = {
        "image": encoded_string,
        "find_position": True,
        "posY": y_center,
        "posX": x_center,
        "width": width,
        "height": height
    }
    return data

# get image and annotation classification data
def get_classification_data(index, first):
    with open("./static/classification/Images/image{}.png".format(index), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    with open("./static/classification/Labels/image{}.txt".format(index), 'r') as file:
        line = file.read()
        present = int(line[1]) == 1
    if first:
        data = {
            "image": encoded_string,
            "present": present,
            "find_position": False,
            "target":"Click yes or no if the desired target is present."
        }
    else:
        data = {
            "image": encoded_string,
            "present": present,
            "find_position": False
        }
    return data

@app.route('/database-ping')
def databaseping():
    from pymongo.mongo_client import MongoClient
    #from pymongo.server_api import ServerApi
    
    try:
        uri = "mongodb+srv://Brain3DVizMember:<password>@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"
        # Create a new client and connect to the server
        client = MongoClient(uri)#, server_api=ServerApi('1'))
        client.admin.command('ping')
        x = "Pinged your deployment.`` You successfully connected to MongoDB!"
    except Exception as e:
        x = "you a bitch"
    return x

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-info-form', methods=['GET'])
def get_info_form():
    # Store response data in MongoDB
    response_data = {
        "formItems": [
            {"value": "Full Name", "type": "string"},
            {"value": "Age", "type": "number"},
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
    full_name = data.get('Full Name')

    # Store response data in MongoDB
    response_data = {
        "user_id": generate_unique_user_id(), #use this id for user-id
        "age": age,
        "sex": sex,
        "full_name": full_name
    }
    users_collection.insert_one(response_data)
    return jsonify(response_data)

@app.route('/game-begin', methods=['GET'])
def game_begin():
    # Other processing...session["index"]
    next_image = get_object_detection_data(0)
    return jsonify(next_image)

@app.route('/test', methods=['GET'])
def test():
    # Other processing...
    return jsonify('Hello')

@app.route('/game-next', methods=['POST'])
def game_next():
    data = request.json
    time = data.get('time')
    num_of_errors = data.get('numOfErrors')
    user_ID = data.get('user-ID')
    user_index = data.get('user-index')
    
    # Store response data in MongoDB
    response_data = {
        "time": time,
        "numOfErrors": num_of_errors,
        "user-ID": user_ID,
        "user-index": user_index
    }
    responses_collection.insert_one(response_data)

    if user_index <= 2:
        next_image = get_object_detection_data(user_index)
    elif user_index == 3:
        next_image = get_classification_data(user_index, True)
    else:
        next_image = get_classification_data(user_index, False)
    return jsonify(next_image)

if __name__ == '__main__':
    app.run(debug=True)
