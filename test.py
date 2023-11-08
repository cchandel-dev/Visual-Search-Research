import base64
index = 16
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
try:
    with open("./static/classification/Images/image{}.png".format(index), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    with open("./static/classification/Labels/image{}.txt".format(index), 'r') as file:
        line = file.read().split()
        present = int(line[0][1]) == 1
        num_shapes = int(line[1])
        conjunction = bool(line[2] == "True")
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
        if index == 0:
            data["max_images"] = 252
        print(conjunction)
except Exception as e:
    print('error', str(e))