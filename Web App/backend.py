from flask import Flask, request, jsonify, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
responses_collection = db["responses"]

sample_form_items = [
    {"value": "Name", "type": "text"},
    {"value": "Age", "type": "number"},
    {"value": "Gender", "type": "select", "options": ["Male", "Female", "Other"]}
]

sample_game_data = {
    "image": "base64_encoded_image_data",
    "posY": 10,
    "posX": 20,
    "width": 100,
    "height": 150
}


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
    return jsonify(sample_game_data)

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
    
    return jsonify(sample_game_data)

if __name__ == '__main__':
    app.run(debug=True)
