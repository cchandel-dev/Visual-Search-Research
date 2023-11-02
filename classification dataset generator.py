from telnetlib import X3PAD
from PIL import Image, ImageDraw
import os, re, random, sys

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

def save_yolo_annotations(annotation, output_path, num_shapes, conjunction, target_color, target_shape):
    with open(output_path, 'w') as file:

            # Write the annotation to the file
            line = f"{annotation}\t{num_shapes}\t{conjunction}\t{target_color}\t{target_shape}\n"
            file.write(line)

def generate_image_and_label( data_number, conjunction, target_available):
    target_color = 'green'
    target_shape = 'square'
    object_x = SPACING/2
    object_y = SPACING/2
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    target_idx = random.randint(0, NUM_SHAPES - 1)
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
            rand = random.random()
            if rand < 0.5:
                object_color = 'green'
                object_shape = 'circle'
            else:
                object_color = 'red'
                object_shape = 'square'
        if idx == target_idx:
            if target_available:
                annotation = [1]
                object_color = target_color
                object_shape = target_shape
            else:
                annotation = [0]
            save_yolo_annotations(annotation, f"static\\classification\\Labels\\{data_number}.txt", NUM_SHAPES, conjunction, target_color, target_shape)
        draw_object(draw, object_shape, object_color, object_x, object_y, idx)

        if object_x < IMAGE_WIDTH - (SPACING + OBJECT_SIZE):
            object_x += SPACING + OBJECT_SIZE
        else:
            object_y += SPACING + OBJECT_SIZE
            object_x = SPACING/2
    # Save the image
    image.save(f"static\\classification\\Images\\{data_number}.png")


# Define const variables
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 1200
MARGIN = 10

#sys.argv[1] is the number of positive cases you would like to generate

if __name__ =='__main__':
    MODES = ['conjunction', 'feature']
    DISTRACTOR_SIZE = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196]
    for MODE in MODES: 
        conjunction = MODE == 'conjunction'
        total_num = int(sys.argv[1])
        for NUM_SHAPES in DISTRACTOR_SIZE:
            NUM_X_SHAPES = NUM_SHAPES ** 0.5
            NUM_Y_SHAPES = NUM_SHAPES ** 0.5
            SPACE_PER_OBJECT = int(IMAGE_WIDTH/NUM_X_SHAPES)
            OBJECT_SIZE = 60
            SPACING = SPACE_PER_OBJECT - OBJECT_SIZE
            print('Working on generating your data...')
            DIR = './static/classification/Images'
            currLen = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            # Ensure a 50/50 split of 0s and 1s
            half_length = total_num // 2
            random_list = [0] * half_length + [1] * half_length
            # Shuffle the list to ensure a random distribution
            random.shuffle(random_list)
            i = 0
            for num in range(currLen, total_num +currLen):
                generate_image_and_label(num, conjunction, random_list[i]==1)
                i+=1


