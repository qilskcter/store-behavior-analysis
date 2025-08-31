from object_detection import detect
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2
import json
# array of res = {start_time, end_time, count}
data = []


def is_inside(points, centroid):
    # check a point that in polygon
    polygon = Polygon(points)
    centroid = Point(centroid)
    return polygon.contains(centroid)


def compare_polygons(polygons, centroid, list_results_by_frame):
    # compare a point inside which polygons?
    for idx, polygon in enumerate(polygons):
        if (is_inside(polygon, centroid)):
            list_results_by_frame[idx]['count'] += 1


def checking(frame, polygons, is_end):
    # (class_ids, scores, boxes) = od.detect(frame)
    # person_boxes = []
    # for index, id in enumerate(class_ids):
    #     #id == 0 (person)
    #     if (id == 0):
    #         person_boxes.append(boxes[index])

    if is_end != True:
        person_boxes = detect(frame)
        list_results_by_frame = []
        for idx in enumerate(polygons):
            res = {
                'count': 0
            }
            list_results_by_frame.append(res)

        if len(person_boxes) == 0:
            data.append(list_results_by_frame)  
        else: 
            for box in person_boxes:
                (x, y, w, h) = box
                cx = int((x + x + w) / 2)
                cy = int((y + y + h) / 2)
                compare_polygons(polygons=polygons, centroid=(cx, cy),
                                list_results_by_frame=list_results_by_frame)
                data.append(list_results_by_frame)       
    else:
        data_to_json()
        data.clear()


def data_to_json():
    json_object = json.dumps(data)
    file_name = 'data/detect_person.json'
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
