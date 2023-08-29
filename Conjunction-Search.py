from PIL import Image, ImageDraw
import random

# Define image dimensions
image_width = 400
image_height = 400

# Define colors
colors = ['red', 'blue', 'green']

# Define shapes
shapes = ['circle', 'square', 'triangle']

# Define number of images to generate
num_images = 100

# Define number of distractors per image
num_distractors = 5

# Create the dataset
for i in range(num_images):
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)
    
    # Generate target
    target_color = random.choice(colors)
    target_shape = random.choice(shapes)
    
    target_x = random.randint(0, image_width - 50)
    target_y = random.randint(0, image_height - 50)
    
    target_size = random.randint(20, 50)
    
    target = None
    
    if target_shape == 'circle':
        target = draw.ellipse((target_x, target_y, target_x + target_size, target_y + target_size), fill=target_color)
    elif target_shape == 'square':
        target = draw.rectangle((target_x, target_y, target_x + target_size, target_y + target_size), fill=target_color)
    elif target_shape == 'triangle':
        target = draw.polygon([(target_x, target_y), (target_x + target_size, target_y), (target_x + target_size // 2, target_y + target_size)], fill=target_color)
    
    # Generate distractors
    for _ in range(num_distractors):
        distractor_color = random.choice([c for c in colors if c != target_color])
        distractor_shape = random.choice([s for s in shapes if s != target_shape])
        
        distractor_x = random.randint(0, image_width - 50)
        distractor_y = random.randint(0, image_height - 50)
        
        distractor_size = random.randint(20, 50)
        
        if distractor_shape == 'circle':
            draw.ellipse((distractor_x, distractor_y, distractor_x + distractor_size, distractor_y + distractor_size), fill=distractor_color)
        elif distractor_shape == 'square':
            draw.rectangle((distractor_x, distractor_y, distractor_x + distractor_size, distractor_y + distractor_size), fill=distractor_color)
        elif distractor_shape == 'triangle':
            draw.polygon([(distractor_x, distractor_y), (distractor_x + distractor_size, distractor_y), (distractor_x + distractor_size // 2, distractor_y + distractor_size)], fill=distractor_color)
    
    # Save the image
    image.save(f"Conjunction Search Images\\conjunction_search_{i}.png")

print("Dataset generation complete.")
