db = client['Reaction-Time']
users_collection = db['users']
responses_collection = db['responses']
print(responses_collection.count())
