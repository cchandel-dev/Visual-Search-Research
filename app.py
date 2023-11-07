import base64, os, time, random, string
from flask import Flask, render_template, request, jsonify
from pymongo.mongo_client import MongoClient

app = Flask(__name__, static_url_path = '/static')
# Configure the app to use sessions
app.config['SESSION_TYPE'] = 'filesystem'

# CONST variables
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400

targets = [
            'click on the red square',
            'click on the blue circle',
            'click on the green square',
            'click on the red triangles',

            'click "Y" for yes or "N" for no - if there is a red square',
            'click "Y" for yes or "N" for no - if there is a blue circle',
            'click "Y" for yes or "N" for no - if there is a green square',
            'click "Y" for yes or "N" for no - if there is a red triangle',
    
]

# uri = "mongodb+srv://Brain3DVizMember:<9GyKqp4b9blclzqJ>@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://Brain3DVizMember:NmwJ5IYmUHDmaQNa@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# point out the collections
db = client['Reaction-Time']
users_collection = db['users']
responses_collection = db['responses']

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
        num_shapes = int(line[5])
        conjunction = bool(line[6])
        target_color = line[7]
        target_shape = line[8]
    data = {
        "image": encoded_string,
        "find_position": True,
        "posY": y_center,
        "posX": x_center,
        "width": width,
        "height": height,
        "num_shapes": num_shapes,
        "conjunction": conjunction,
        "target_color": target_color,
        "target_shape": target_shape
    }

    #if index >= 35 and index < 70:
    data['check_errors'] = False

    if index == 0:
        data['target'] = targets[0]
    elif index == 28:
        data['target'] = targets[1]
    elif index == 56:
        data['target'] = targets[2]
    elif index == 84:
        data['target'] = targets[3]
    return data

# get image and annotation classification data
def get_classification_data(index):
    with open("./static/classification/Images/image{}.png".format(index), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    with open("./static/classification/Labels/image{}.txt".format(index), 'r') as file:
        line = file.read().split()
        present = int(line[0][1]) == 1
        num_shapes = int(line[1])
        conjunction = bool(line[2])
        target_color = line[3]
        target_shape = line[4]
    data = {
        "image": encoded_string,
        "present": present,
        "find_position": False,
        "num_shapes": num_shapes,
        "conjunction": conjunction,
        "target_color": target_color,
        "target_shape": target_shape
    }
    if index == 0:
        data['target'] = targets[4]
    elif index == 28:
        data['target'] = targets[5]
    elif index == 56:
        data['target'] = targets[6]
    elif index == 84:
        data['target'] = targets[7]
    return data

@app.route('/database-ping')
def databaseping():
    try:        
        client.admin.command('ping')
        data = {
            "test_signal": True
        }
        users_collection.insert_one(data)
        responses_collection.insert_one(data)
        x = "Pinged your deployment. You successfully connected to MongoDB! Feel free to check MongoDB for collection information"
    except Exception as e:
        x = e.__str__()
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
            {"value": "Year of Study", "type": "select", "options": ["1", "2", "3","4", "N/A"]},
            {"value": "Task Type", "type": "select", "options": ["detection", "pointing"]}
        ]
    }
    return jsonify(response_data)

@app.route('/save-form-data', methods=['POST'])
def save_form_data():
    # Other processing...
    data = request.json
    task = data.get('Task Type')
    year = data.get('Year of Study')
    full_name = data.get('Full Name')
    userID = generate_unique_user_id()
    # Store response data in MongoDB
    response_data = {
        "user_id": userID, #use this id for user-id
        "task_type": task,
        "year_of_study": year,
        "full_name": full_name
    }
    data["user_id"] = userID
    users_collection.insert_one(data)
    return jsonify(response_data)

# @app.route('/game-begin', methods=['GET'])
# def game_begin():
#     # Other processing...session["index"]
#     next_image = get_object_detection_data(0)
#     next_image["max_images"] = 252
#     return jsonify(next_image)

@app.route('/test', methods=['GET'])
def test():
    # Other processing...
    return jsonify('Hello')

@app.route('/game-next', methods=['POST'])
def game_next():
    data = request.json

    user_index = data.get('user-index')
    task_type = data.get('task_type')
    responses_collection.insert_one(data)

    try:
        if task_type == "pointing":
            next_image = get_object_detection_data(user_index)
        else:
            next_image = get_classification_data(user_index)

        # if user_index == 0:
        #     next_image["max_images"] = 252

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    return jsonify(next_image)

if __name__ == '__main__':
    app.run(debug=True)
0