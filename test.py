import base64
index = 0
with open("./static/classification/Images/image{}.png".format(index), "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
with open("./static/classification/Labels/image{}.txt".format(index), 'r') as file:
    line = file.read()
    present = int(line[1]) == 1
    num_shapes = int(line[2])
    conjunction = bool(line[3])
    target_color = line[4]
    target_shape = line[5]
    print(line)