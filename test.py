import base64
index = 0
with open("./static/classification/Images/image{}.png".format(index), "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
with open("./static/classification/Labels/image{}.txt".format(index), 'r') as file:
    line = file.read().split()
    present = int(line[0][1]) == 1
    num_shapes = int(line[1])
    conjunction = bool(line[2])
    target_color = line[3]
    target_shape = line[4]
    print(line)
    print(present, num_shapes, conjunction, target_color, target_shape)