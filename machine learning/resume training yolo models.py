import os, torch
from ultralytics import YOLO, settings

# Update multiple settings
settings.update({
                'weights_dir': 'C:\\Users\\cchan\\Visual-Search-Research\\machine learning\\object detection models',
                'runs_dir': 'C:\\Users\\cchan\\Visual-Search-Research\\machine learning\\runs',
                })
# Load a model
file_path = str(os.path.join(os.getcwd(),'runs\\detect\\train14\\weights\\last.pt'))
print(file_path)
model = YOLO(file_path)
# Resume training
results = model.train(resume=True)