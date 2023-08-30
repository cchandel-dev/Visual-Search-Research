from telnetlib import X3PAD
from PIL import Image, ImageDraw
import random, sys

# Define const variables
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
SPACING = 20
OBJECT_SIZE = 30
MARGIN = 10
X_SHAPES = int(IMAGE_WIDTH/(SPACING + OBJECT_SIZE))
Y_SHAPES = int(IMAGE_HEIGHT/(SPACING + OBJECT_SIZE))
NUM_SHAPES = X_SHAPES * Y_SHAPES

def draw_object(draw, object_shape, object_color, object_x, object_y, number):
    if object_shape == 'circle':
        draw.ellipse((object_x, object_y, object_x + OBJECT_SIZE, object_y + OBJECT_SIZE), fill=object_color)
    elif object_shape == 'square':
        draw.rectangle((object_x, object_y, object_x + OBJECT_SIZE, object_y + OBJECT_SIZE), fill=object_color)
    elif object_shape == 'triangle':
        draw.polygon([(object_x, object_y), (object_x + OBJECT_SIZE, object_y), (object_x + OBJECT_SIZE // 2, object_y + OBJECT_SIZE)], fill=object_color)
    # Calculate the position to print the number (center of the shape)
    number_x = object_x + OBJECT_SIZE // 3
    number_y = object_y + OBJECT_SIZE // 3
    
    # Print the number onto the shape
    draw.text((number_x, number_y), str(number), fill=(255, 255, 255))  # You can adjust fill color

def save_yolo_annotations(annotation_list, image_width, image_height, output_path):
    with open(output_path, 'w') as file:
        for annotation in annotation_list:
            class_name, x_center, y_center, width, height = annotation

            # Convert coordinates to YOLO format (normalized)
            x_center /= IMAGE_WIDTH
            y_center /= IMAGE_HEIGHT
            width /= IMAGE_WIDTH
            height /= IMAGE_HEIGHT

            # Get class index based on class name (you need to define this mapping)
            class_index = class_name

            # Write the annotation to the file
            line = f"{class_index} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            file.write(line)

def generate_image_and_label(target_shape, target_color, data_number, conjunction):
    object_x = SPACING/2
    object_y = SPACING/2
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    target_idx = random.randint(0, NUM_SHAPES)
    objects = {'green': 'circle',
           'red': 'square',
           'blue': 'triangle'}
    name = 'conjunction' if conjunction else 'feature'
    # Generate shapes
    for idx in range(NUM_SHAPES):
        if not conjunction: # feature
            object_color = 'green' # distractor shape
            object_shape = 'circle'# distractor color
        else: # conjunction
            object_color = random.choice(list(objects.keys())) #distractor color can be target color
            # Exclude the current target_shape from the list of available shapes
            available_shapes = [shape for shape in objects.values() if shape != target_shape] if object_color == target_color else list(objects.values())
            # Choose a new target_shape randomly from the available shapes
            object_shape = random.choice(available_shapes)

        if idx == target_idx:
            object_color = target_color
            object_shape = target_shape 
            annotation = [[0, int(object_x + OBJECT_SIZE/2), int(object_y + OBJECT_SIZE/2), OBJECT_SIZE, OBJECT_SIZE]]
            save_yolo_annotations(annotation, IMAGE_WIDTH, IMAGE_HEIGHT, f"Labels\\{name} {data_number}.txt")
        draw_object(draw, object_shape, object_color, object_x, object_y, idx)

        if object_x < IMAGE_WIDTH - (SPACING + OBJECT_SIZE):
            object_x += SPACING + OBJECT_SIZE
        else:
            object_y += SPACING + OBJECT_SIZE
            object_x = SPACING/2
    # Save the image
    image.save(f"Images\\{name} {data_number}.png")

#sys.argv[1] is 'conjuntion' or 'feature' default is feature
#sys.argv[2] is target shape default is 'square'
#sys.argv[3] is target color default is 'green'
#sys.argv[4] is the number of datapoints you would like to generate
if __name__ =='__main__':
    conjunction = sys.argv[1] == 'conjunction'
    print('Working on generating your data...')
    for num in range(int(sys.argv[4])):
        generate_image_and_label(sys.argv[2], sys.argv[3], num, conjunction)
    print('Dataset generated.')