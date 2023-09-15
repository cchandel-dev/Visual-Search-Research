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
    number_x = object_x + OBJECT_SIZE // 3
    number_y = object_y + OBJECT_SIZE // 3
    
    # Print the number onto the shape
    #draw.text((number_x, number_y), str(number), fill=(255, 255, 255))  # You can adjust fill color

def save_yolo_annotations(annotation, output_path):
    with open(output_path, 'w') as file:
            present = annotation

            # Write the annotation to the file
            line = f"{present}\n"
            file.write(line)

def generate_image_and_label(target_shape, target_color, data_number, probability, conjunction):
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
            object_color = random.choice(list(objects.keys())) #distractor color can be target color
            # Exclude the current target_shape from the list of available shapes
            available_shapes = [shape for shape in objects.values() if shape != target_shape] if object_color == target_color else list(objects.values())
            # Choose a new target_shape randomly from the available shapes
            object_shape = random.choice(available_shapes)
        rand = random.random()
        if idx == target_idx:
            if rand <= probability: 
                annotation = [1]    
                object_color = target_color
                object_shape = target_shape
            else:
                annotation = [0]       
            save_yolo_annotations(annotation, f"static\\classification\\Labels\\image{data_number}.txt")
        draw_object(draw, object_shape, object_color, object_x, object_y, idx)

        if object_x < IMAGE_WIDTH - (SPACING + OBJECT_SIZE):
            object_x += SPACING + OBJECT_SIZE
        else:
            object_y += SPACING + OBJECT_SIZE
            object_x = SPACING/2
    # Save the image
    image.save(f"static\\classification\\Images\\image{data_number}.png")


# Define const variables
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
MARGIN = 10

#sys.argv[1] is 'conjuntion' or 'feature' default is feature
#sys.argv[2] is target shape default is 'square'
#sys.argv[3] is target color default is 'green'
#sys.argv[4] is the number of datapoints you would like to generate
#sys.argv[5] is the number of positive cases you would like to generate
#sys.argv[6] is the number of shapes per image
if __name__ =='__main__':
    conjunction = sys.argv[1] == 'conjunction'
    positive_num = int(sys.argv[5])
    total_num = int(sys.argv[4])
    NUM_SHAPES = int(sys.argv[6])
    NUM_X_SHAPES = NUM_SHAPES ** 0.5
    NUM_Y_SHAPES = NUM_SHAPES ** 0.5
    SPACE_PER_OBJECT = int(IMAGE_WIDTH/NUM_X_SHAPES)
    OBJECT_SIZE = 30
    SPACING = SPACE_PER_OBJECT - OBJECT_SIZE
    probability = float(positive_num/total_num)
    print('probability figure is: ', probability)
    print('Working on generating your data...')
    DIR = './static/classification/Images'
    currLen = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    for num in range(currLen, total_num +currLen):
        generate_image_and_label(sys.argv[2], sys.argv[3], num, probability, conjunction)
    print('Dataset generated.')



