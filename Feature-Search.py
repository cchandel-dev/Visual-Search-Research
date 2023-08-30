from PIL import Image, ImageDraw
import random


def save_yolo_annotations(annotation_list, image_width, image_height, output_path):
    with open(output_path, 'w') as file:
        for annotation in annotation_list:
            class_name, x_center, y_center, width, height = annotation

            # Convert coordinates to YOLO format (normalized)
            x_center /= image_width
            y_center /= image_height
            width /= image_width
            height /= image_height

            # Get class index based on class name (you need to define this mapping)
            class_index = class_name

            # Write the annotation to the file
            line = f"{class_index} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
            file.write(line)


# Define image dimensions
image_width = 400
image_height = 400

# Define number of images to generate
num_images = 100

# Define number of distractors per image
num_distractors = 63
spacing = 50
object_size = 30

# Define the target
target_color = 'green'
target_shape = 'square'
name = 'feature_search_'
# Create the dataset
for i in range(num_images):
    x = 0
    y = 0
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    target_idx = random.randint(0, num_distractors)

    # Generate shapes
    for idx in range(num_distractors + 1):
        object_color = 'green'
        object_shape = 'circle'
        if idx == target_idx:
            object_color = target_color
            object_shape = target_shape     
            annotation = [[0, int(object_x + object_size/2), int(object_y + object_size/2), object_size, object_size]]
            save_yolo_annotations(annotation, image_width, image_height, f"Labels\\{name}{i}.txt")
        object_x = x
        object_y = y
        
        if x < image_width - 50:
            x += 50
            print('x', x)
        else:
            y += 50
            x = 0
            print('y', y)
    


        if object_shape == 'circle':
            draw.ellipse((object_x, object_y, object_x + object_size, object_y + object_size), fill=object_color)
        elif object_shape == 'square':
            draw.rectangle((object_x, object_y, object_x + object_size, object_y + object_size), fill=object_color)
        elif object_shape == 'triangle':
            draw.polygon([(object_x, object_y), (object_x + object_size, object_y), (object_x + object_size // 2, object_y + object_size)], fill=object_color)
        
    # Save the image
    image.save(f"Conjunction Search Images\\{name}{i}.png")

print("Dataset generation complete.")


