from PIL import Image, ImageDraw
import random

# Define image dimensions
image_width = 400
image_height = 400

# Define objects
objects = {'green': 'circle',
           'red': 'square',
           'blue': 'triangle'}

# Define number of images to generate
num_images = 100

# Define number of distractors per image
num_distractors = 63
spacing = 50

# Define the target
target_color = 'green'
target_shape = 'square'

# Create the dataset
for i in range(num_images):
    x = 0
    y = 0
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    target_idx = random.randint(0, num_distractors)

    # Generate shapes
    for idx in range(num_distractors + 1):
        object_color = target_color
        object_shape = target_shape
        if idx != target_idx:
            object_color = random.choice(list(objects.keys()))
            object_shape = objects[object_color]
        object_x = x
        object_y = y
        
        if x < image_width - 50:
            x += 50
            print('x', x)
        else:
            y += 50
            x = 0
            print('y', y)
    
        object_size = 30 #random.randint(20, 50)
        
        if object_shape == 'circle':
            draw.ellipse((object_x, object_y, object_x + object_size, object_y + object_size), fill=object_color)
        elif object_shape == 'square':
            draw.rectangle((object_x, object_y, object_x + object_size, object_y + object_size), fill=object_color)
        elif object_shape == 'triangle':
            draw.polygon([(object_x, object_y), (object_x + object_size, object_y), (object_x + object_size // 2, object_y + object_size)], fill=object_color)
        
    # Save the image
    image.save(f"Conjunction Search Images\\conjunction_search_{i}.png")

print("Dataset generation complete.")
