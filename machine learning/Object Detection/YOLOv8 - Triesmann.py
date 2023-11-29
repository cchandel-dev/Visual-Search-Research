from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
model = YOLO('C:\\Users\\cchan\\computer-vision\\runs\\detect\\train9\\weights\\best.pt')

# Display model information (optional)
model.info()

# Train the model on the COCO8 example dataset for 100 epochs
results = model.train(data='data.yaml', epochs=100, imgsz=600, verbose = True, save_dir="C:\\Users\\cchan\\Laproscopic Surgery Work\\Surgical Tool - Object Detection\\runs\\detect", patience = 20)

# Run inference with the YOLOv8n model on the test image
model.predict("C:\\Users\\cchan\\Visual-Search-Research\\machine learning\\Surgical Tool - Object Detection\\valid\\images\\image28.png", save=True, imgsz=320, conf=0.35)
# model.predict('C:\\Users\\cchan\\Laproscopic Surgery Work\\Private Image Annotator\\data\\images\\023.jpg', save=True, imgsz=320, conf=0.7)