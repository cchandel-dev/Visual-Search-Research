import os, torch, math, time, glob
from ultralytics import YOLO, RTDETR, settings
from datetime import datetime
from ultralytics.utils.benchmarks import benchmark
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Brain3DVizMember:NmwJ5IYmUHDmaQNa@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['Reaction-Time']
ml_collection = db['machine-learning']

class TrialRunner:
    def __init__(self):
        self.model_folder = 'C:\\Users\\cchan\\Downloads\\object detection models'
        # Filter to keep only image files (you can modify this condition based on your file types)
        self.model_paths = os.listdir(self.model_folder)
        self.test_data_path = 'C:\\Users\\cchan\\Visual-Search-Research\\static\\object-detection'
        self.test_images_paths = os.listdir(os.path.join(self.test_data_path, "images"))
        self.current_index = 0
        self.current_model = None
        self.user = None
        self.cpu = True
        self.device = None
        self.timestamp = datetime.now()

    def object_detection_loop(self):
        print('in the loop')
        print(self.model_paths)
        for model_path in self.model_paths:
            print(model_path)
            model_metrics = {}
            model_metrics['model_name'] = model_path.split(' ')[0]
            model_metrics['num_epochs'] = int(model_path.split(' ')[1])
            if model_metrics['model_name'][:4] == 'yolo':
                model_metrics['one-stager'] = True
                self.current_model = YOLO(os.path.join(self.model_folder, model_path, 'weights', 'best.pt'))
            else:
                model_metrics['one-stager'] = False
                self.current_model = RTDETR(os.path.join(self.model_folder, model_path, 'weights', 'best.pt'))
            # let's assume they are already trained.
            for test_image_path in self.test_images_paths:
                # let's say we are happy with these parameters as our input
                results = self.current_model.predict(   
                                                        source = os.path.join(self.test_data_path,"images", test_image_path), # might need the full path here
                                                        device ='cpu', 
                                                        save = False,
                                                        imgsz = 640,
                                                        conf = 0.35,
                                                    )
                # now let's figure out how accurate the prediction was and log anything of note that results might hold (ie inference speed, number of predictions per confidence range, etc.)
                image_metrics = results.__getitem__(0).speed
                label_folder = os.path.join(self.test_data_path, "labels")
                lines = ""
                with open(os.path.join(label_folder, test_image_path[:-4]+".txt"), 'r') as lbls:
                    lines = lbls.readlines()
                # clean up the formatting for both the annotations and predictions
                annotations = lines_to_boxes(lines)
                # num_shapes, conjunction/feature, target color, target shape, num green circles, num red square, num green squares
                line = lines[0].split()
                annotations_addendum = [int(line[5]), line[6] == 'True', line[7], line[8], int(line[9]), int(line[10]), int(line[11])]
                predictions = xywhn_to_yolo_format(results.__getitem__(0).boxes.xywhn, results.__getitem__(0).boxes.cls, results.__getitem__(0).boxes.conf)
                #REMINDER: this assumes your model works pretty well and now you just want to gather more performance related data
                aligning = align_annotations(predictions, annotations)
                image_metrics["difference_anot-pred"] = len(annotations) - len(predictions)
                image_metrics["length-annotations"] = len(annotations)
                image_metrics["length-predictions"] = len(predictions)
                image_metrics["pairs_anot-pred"] = len(aligning)
                image_metrics["num_shapes"] = annotations_addendum[0]
                image_metrics["conjunction"] = annotations_addendum[1]
                image_metrics["target_color"] = annotations_addendum[2]
                image_metrics["target_shape"] = annotations_addendum[3]
                image_metrics["num_green_circle"] = annotations_addendum[4]
                image_metrics["num_red_square"] = annotations_addendum[5]
                image_metrics["num_green_square"] = annotations_addendum[6]
                if len(aligning) > 0:
                    for align_iou in aligning:
                        prediction_metrics = {}
                        # class equality
                        prediction_metrics["class-equality"] = predictions[align_iou[0]][4] == annotations[align_iou[1]][4]
                        # centre point distance
                        x1 = predictions[align_iou[0]][0]
                        x2 = annotations[align_iou[1]][0]
                        y1 = predictions[align_iou[0]][1]
                        y2 = annotations[align_iou[1]][1]
                        prediction_metrics["euclidean-distance-between-centers"] = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                        prediction_metrics["x-distance-between-centers"] = x1 - x2
                        prediction_metrics["y-distance-between-centers"] = y1 - y2
                        # intersection over union
                        prediction_metrics["intersection-over-union"] = align_iou[2]
                        # confidence metrics
                        prediction_metrics["confidence"] = align_iou[3]
                        # prediction made
                        prediction_metrics["at_least_one"] = True
                    else:
                        prediction_metrics["at_least_one"] = False
                    #FOR EACH BOUNDING BOX WE SEND ONE MESSAGE
                    msg = {**prediction_metrics, **image_metrics, **model_metrics}
                    ml_collection.insert_one(msg)

def xywhn_to_yolo_format(xywh_tensor, cls_tensor, conf_tensor):
    """
    Convert bounding boxes from xywh format to YOLO format.

    Parameters:
    - xywh_tensor: Tensor containing bounding boxes in xywh format.

    Returns:
    - yolo_boxes: List of bounding boxes in YOLO format.
    """
    # print("xywh_tensor:", xywh_tensor)
    # print("cls_tensor:", cls_tensor)
    yolo_boxes = []
    cls = cls_tensor.tolist()
    conf = conf_tensor.tolist()
    # print("cls_list:", cls)
    for idx in range(len(xywh_tensor)):
        box = xywh_tensor[idx].tolist()
        # print("box:", box)
        x_center, y_center, width, height = box
        # Convert to YOLO format (x_center, y_center, width, height)
        yolo_box = [
            x_center,
            y_center,
            width,
            height,
            int(cls[idx]),
            float(conf[idx])
        ]
        # print("yolo_box:", yolo_box)
        yolo_boxes.append(yolo_box)
    return yolo_boxes

def lines_to_boxes(lines):
    yolo_boxes = []
    for line in lines:
        line = line.split()
        yolo_boxes.append([float(line[1]), float(line[2]), float(line[3]), float(line[4]), int(line[0])])
    return yolo_boxes

def align_annotations(predictions, annotations, threshold=0.35):
    """
    Align predicted bounding boxes with ground truth bounding boxes based on IoU.

    Parameters:
    - predictions: List of predicted bounding boxes in YOLO format.
    - annotations: List of ground truth bounding boxes in YOLO format.
    - threshold: IoU threshold for matching.

    Returns:
    - aligned_pairs: List of tuples (prediction_index, annotation_index) representing aligned pairs.
    """
    aligned_pairs = []
    max_conf_idx = 0
    if len(predictions) == 0:
        return aligned_pairs
    max_conf = predictions[max_conf_idx][5]
    for pred_index in range(len(predictions)):
        if predictions[pred_index][5] > max_conf:
            max_conf_idx = pred_index
            max_conf =  predictions[max_conf_idx][5]
    iou = calculate_iou(predictions[max_conf_idx][0:4], annotations[0][0:4]) #only need these four labels
    aligned_pairs.append((pred_index, 0, iou, max_conf))
    return aligned_pairs

def calculate_iou(box1, box2):
    """
    Calculate Intersection over Union (IoU) between two bounding boxes.

    Parameters:
    - box1, box2: Bounding boxes in YOLO format (x_center, y_center, width, height).

    Returns:
    - IoU: Intersection over Union value.
    """
    # Convert YOLO format to (x_min, y_min, x_max, y_max) format
    box1 = [
        box1[0] - box1[2] / 2,
        box1[1] - box1[3] / 2,
        box1[0] + box1[2] / 2,
        box1[1] + box1[3] / 2
    ]
    box2 = [
        box2[0] - box2[2] / 2,
        box2[1] - box2[3] / 2,
        box2[0] + box2[2] / 2,
        box2[1] + box2[3] / 2
    ]

    # Calculate intersection coordinates
    x_intersection = max(box1[0], box2[0])
    y_intersection = max(box1[1], box2[1])
    w_intersection = max(0, min(box1[2], box2[2]) - x_intersection)
    h_intersection = max(0, min(box1[3], box2[3]) - y_intersection)

    # Calculate area of intersection and union
    area_intersection = w_intersection * h_intersection
    area_union = (box1[2] - box1[0]) * (box1[3] - box1[1]) + (box2[2] - box2[0]) * (box2[3] - box2[1]) - area_intersection

    # Calculate IoU
    iou = area_intersection / area_union if area_union > 0 else 0.0

    return iou

if __name__ == '__main__':
    tr = TrialRunner()
    print('checkpoint')
    tr.object_detection_loop()