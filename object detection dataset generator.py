from telnetlib import X3PAD
from PIL import Image, ImageDraw
import os, random, sys


def draw_object(draw, object_shape, object_color, object_x, object_y, number):
    if object_shape == 'circle':
        draw.ellipse((object_x, object_y, object_x + OBJECT_SIZE, object_y + OBJECT_SIZE), fill=object_color)
    elif object_shape == 'square':
        draw.rectangle((object_x, object_y, object_x + OBJECT_SIZE, object_y + OBJECT_SIZE), fill=object_color)
    elif object_shape == 'triangle':
        draw.polygon([(object_x, object_y), (object_x + OBJECT_SIZE, object_y), (object_x + OBJECT_SIZE // 2, object_y + OBJECT_SIZE)], fill=object_color)
    # Calculate the position to print the number (center of the shape)
    # number_x = object_x + OBJECT_SIZE // 3
    # number_y = object_y + OBJECT_SIZE // 3
    
    # Print the number onto the shape
    #draw.text((number_x, number_y), str(number), fill=(255, 255, 255))  # You can adjust fill color

def save_yolo_annotations(annotation_list, image_width, image_height, output_path, num_shapes, conjunction, target_color, target_shape, green_circle, red_square, green_square):
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
            line = f"{class_index}\t{x_center:.6f}\t{y_center:.6f}\t{width:.6f}\t{height:.6f}\t{num_shapes}\t{conjunction}\t{target_color}\t{target_shape}\t{green_circle}\t{red_square}\t{green_square}\n"
            file.write(line)

def generate_image_and_label(data_number, conjunction):
    target_shape = 'square'
    target_color = 'green'
    object_x = SPACING/2
    object_y = SPACING/2
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    target_idx = random.randint(0, NUM_SHAPES - 1)
    objects = {'green': 'circle',
           'red': 'square',
           'blue': 'triangle'}
    name = 'conjunction' if conjunction else 'feature'
    annotation = [[0, 0, 0, 0, 0]]
    green_circle = 0
    red_square = 0
    green_square = 0
    # Generate shapes
    for idx in range(NUM_SHAPES):
        if not conjunction: # feature
            object_color = 'green' # distractor shape
            object_shape = 'circle'# distractor color
        else: # conjunction
            rand = random.random()
            if rand < 0.5:
                object_color = 'green'
                object_shape = 'circle'
            else:
                object_color = 'red'
                object_shape = 'square'
        if idx == target_idx:
            object_color = target_color
            object_shape = target_shape
            annotation = [[0, int(object_x + OBJECT_SIZE/2), int(object_y + OBJECT_SIZE/2), OBJECT_SIZE, OBJECT_SIZE]]
            green_square = 1

        draw_object(draw, object_shape, object_color, object_x, object_y, idx)
        # count the types of distractors
        if object_shape == 'circle' and object_color == 'green':
            green_circle += 1
        elif object_shape == 'square' and object_color == 'red':
            red_square += 1
        if object_x < IMAGE_WIDTH - (SPACING + OBJECT_SIZE):
            object_x += SPACING + OBJECT_SIZE
        else:
            object_y += SPACING + OBJECT_SIZE
            object_x = SPACING/2
    # Save the image
    image.save(f"static\\object-detection\\Images\\{data_number}.png")
    save_yolo_annotations(annotation, IMAGE_WIDTH, IMAGE_HEIGHT, f"static\\object-detection\\Labels\\{data_number}.txt", NUM_SHAPES, conjunction, target_color, target_shape, green_circle, red_square, green_square)


# Define const variables
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 1200
MARGIN = 10


#sys.argv[1]  is the number of datapoints you would like to generate
if __name__ =='__main__':
    MODES = ['conjunction', 'feature']
    DISTRACTOR_SIZE = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
    for MODE in MODES: 
        conjunction = MODE == 'conjunction'
        for NUM_SHAPES in DISTRACTOR_SIZE:
            NUM_X_SHAPES = NUM_SHAPES ** 0.5
            NUM_Y_SHAPES = NUM_SHAPES ** 0.5
            SPACE_PER_OBJECT = int(IMAGE_WIDTH/NUM_X_SHAPES)
            OBJECT_SIZE = 60
            SPACING = SPACE_PER_OBJECT - OBJECT_SIZE
            print('Working on generating your data...')
            # path joining version for other paths
            DIR = '.\\static\\object-detection\\Images'
            currLen = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            for num in range(currLen, currLen + int(sys.argv[1])):
                generate_image_and_label(num, conjunction)
    print('Dataset generated.')