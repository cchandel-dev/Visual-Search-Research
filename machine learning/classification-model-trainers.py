import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

# Define the number of classes
NUM_CLASSES = 2
DATA_DIR = 'C:\\Users\\cchan\\Visual-Search-Research\\static'
TRAIN_DIR = os.path.join(DATA_DIR, 'classification - train')
TEST_DIR = os.path.join(DATA_DIR, 'classification - test')
VALIDATE_DIR = os.path.join(DATA_DIR, 'classification - validate')
# Load and preprocess images
def load_and_preprocess_image(image_path):
    img = load_img(os.path.join(TRAIN_DIR, 'Images', image_path), target_size=(224, 224))  # Adjust the target size based on your requirements
    img_array = img_to_array(img) / 255.0  # Normalize the pixel values
    return img_array

# Load and preprocess labels
def load_and_preprocess_label(label_path):
    with open(os.path.join(TRAIN_DIR, 'Labels', label_path), 'r') as file:
        for line in file:
            line = line.split(' ')
    label = int(line[0][1])
    # Perform one-hot encoding
    one_hot_label = to_categorical(label, num_classes=NUM_CLASSES)
    return one_hot_label

# Define a custom data generator
def data_generator(data_directory, batch_size):
    # Define data directories 
    images_path = os.listdir(os.path.join(data_directory, 'images'))
    labels_path = os.listdir(os.path.join(data_directory, 'labels'))
    num_samples = len(labels_path)
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_image_paths = images_path[offset:offset+batch_size]
            batch_label_paths = labels_path[offset:offset+batch_size]
            batch_images= [load_and_preprocess_image(image_path) for image_path in batch_image_paths]
            batch_labels= [load_and_preprocess_label(label_path) for label_path in batch_label_paths]
            yield np.array(batch_images), np.array(batch_labels)


# Define test, train and validate
batch_size = 32
total_train_sample = len(os.listdir(os.path.join(TRAIN_DIR, 'images')))
total_validate_sample = len(os.listdir(os.path.join(VALIDATE_DIR, 'images')))
train_generator = data_generator(TRAIN_DIR, batch_size)
test_generator = data_generator(TEST_DIR, batch_size)
validate_generator = data_generator(VALIDATE_DIR, batch_size)


model_names = [  'ResNet50', 'ResNet101', 'ResNet152', 'VGG16',
            'VGG19', 'DenseNet121', 'DenseNet169','DenseNet201',
            'MobileNet', 'MobileNetV2', 'MobileNetV3']
epochs = [10, 50, 100, 500, 1000]
for model_name in model_names:
    for epoch in epochs:
        print('training {}'.format(model_name))
        # Dynamically get the model by name
        model_fn = getattr(tf.keras.applications, model_name)
        base_model = model_fn(weights=None, include_top=False, input_shape=(224, 224, 3))

        # Add your own classification layers
        x = base_model.output
        x = GlobalAveragePooling2D()(x)  # Add pooling if needed
        x = Dense(1024, activation='relu')(x)  # dense layers
        x = Dense(512, activation='relu')(x)  # dense layers
        x = Dense(256, activation='relu')(x)  # dense layers
        x = Dense(128, activation='relu')(x)  # dense layers
        x = Dense(64, activation='relu')(x)  # dense layers
        x = Dense(32, activation='relu')(x)  # dense layers
        x = Dense(16, activation='relu')(x)  # dense layers
        x = Dense(8, activation='relu')(x)  # dense layers
        predictions = Dense(NUM_CLASSES, activation='softmax')(x)  # Output layer

        model = Model(inputs=base_model.input, outputs=predictions)

        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Train the model
        model.fit(
                    train_generator,
                    steps_per_epoch= total_train_sample//batch_size,
                    epochs=10,
                    validation_data=validate_generator,
                    validation_steps= total_validate_sample//batch_size
               )
        
        # File naming based on weight setting
        filename = f'{model_name}_{epoch}.h5'
        
        # Save the model to a file
        model.save(filename)
