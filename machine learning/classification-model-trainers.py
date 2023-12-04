import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tensorflow.keras.utils import to_categorical

# Define the number of classes
NUM_CLASSES = 2

# Load and preprocess images
def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(299, 299))  # Adjust the target size based on your requirements
    img_array = img_to_array(img) / 255.0  # Normalize the pixel values
    return img_array

# Load and preprocess labels
def load_and_preprocess_label(label_path):
    with open(label_path, 'r') as file:
        for line in file:
            line = line.split(' ')
    label = int(line[0][1])
    # Perform one-hot encoding
    one_hot_label = to_categorical(label, num_classes=NUM_CLASSES)
    return one_hot_label

# Define a custom data generator
def data_generator(data_directory, batch_size=32):
    # Define data directories 
    images_path = os.path.join(data_directory, 'images')
    labels_path = os.path.join(data_directory, 'labels')
    num_samples = len(os.path.dir(labels_path))
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_image_paths = images_path[offset:offset+batch_size]
            batch_label_paths = labels_path[offset:offset+batch_size]
            batch_images= [load_and_preprocess_image(image_path) for image_path in batch_image_paths]
            batch_labels= [load_and_preprocess_label(label_path) for label_path in batch_label_paths]
            yield np.array(batch_images), np.array(batch_labels)


# Define test, train and validate
train_generator = data_generator('C:\\Users\\cchan\\Visual-Search-Research\\static\\classification - train')
test_generator = data_generator('C:\\Users\\cchan\\Visual-Search-Research\\static\\classification - test')
validate_generator = data_generator('C:\\Users\\cchan\\Visual-Search-Research\\static\\classification - validate')


model_names = [  'ResNet50', 'ResNet101', 'ResNet152', 'VGG16',
            'VGG19', 'DenseNet121', 'DenseNet169','DenseNet201',
            'MobileNet', 'MobileNetV2', 'MobileNetV3']
weight_settings = ['imagenet', 'None']
for model_name in model_names:
    for weight_setting in weight_settings:
        # Dynamically get the model by name
        model_fn = getattr(tf.keras.applications, model_name)
        model = model_fn(
                            weights = weight_setting,
                            classes = NUM_CLASSES,
                            pooling = True,
                        )
        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Train the model
        model.fit(
                    train_generator,
                    test_generator,
                    steps_per_epoch=len(train_generator),
                    epochs=10,
                    validation_data=validate_generator,
                    validation_steps=len(validate_generator)
               )
        
        # File naming based on weight setting
        weight_str = 'imagenet' if weight_setting == 'imagenet' else 'no_weights'
        filename = f'{model_name}_{weight_str}.h5'
        
        # Save the model to a file
        model.save(filename)
