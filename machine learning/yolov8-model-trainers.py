from ultralytics import YOLO, RTDETR, settings
from multiprocessing import Process, freeze_support

# models
yolo_models = ['yolov8s', 'yolov8m', 'yolov8l']
detr_models = ['rtdetr-l', 'rtdetr-x']
model_families = [yolo_models, detr_models]

#epochs
epochs = [1, 25, 50, 75, 100]

# Update multiple settings
settings.update({
                'weights_dir': 'C:\\Users\\cchandel\\Visual-Search-Research\\machine learning\\object detection models',
                'runs_dir': 'C:\\Users\\cchandel\\Visual-Search-Research\\machine learning\\runs',
                })

def training_fnc_multiprocessing():
    # Your multiprocessing logic goes here
    print('check 1')
    for model_family in model_families:
        print('check 2')
        for model_name in model_family:
            print('check 3')
            for epoch in epochs:
                print('check 4')
                try:
                    print('check 5')
                    model = RTDETR(model_name+'.pt')
                    print('check 6')
                    print(model_name, model_name[1], model_name[1][:4])
                    if model_name[:4] == 'yolo':
                        model = YOLO(model_name+'.pt')
                        print('check 7')
                    print('training {}.pt'.format(model_name))
                    results = model.train(data='data.yaml', epochs=epoch, imgsz=600, verbose = True, patience = int(epoch*0.3), name = model_name + ' ' + str(epoch))
                except Exception as e:
                    print("There was an error training {} at {} epoch setting.\nThe error is {}".format(model_name, epoch, e))
                    raise e

if __name__ == '__main__':
    freeze_support()
    # Start your processes here
    process = Process(target=training_fnc_multiprocessing)
    process.start()
    process.join()  # Optionally wait for the process to finish




