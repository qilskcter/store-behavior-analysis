import cv2
import numpy as np
from imutils.video import VideoStream
from yolodetect import YoloDetect
import json

video = VideoStream('./dataset/video.mp4').start()

# chứa các điểm người dùng chọn để tạo đa giác
currentPoints = []
polygons = []
file_name = 'polygons.json'

# new model Yolo
model = YoloDetect()


# nếu bấm chuột trái, điểm points sẽ tự nối lại bằng hàm append


def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])


# draw polygon


def draw_polygon(frame, points):
    for point in points:
        frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)

    frame = cv2.polylines(frame, [np.int32(points)],
                          False, (255, 0, 0), thickness=2)
    return frame


# set Yolo được phép detect chưa
detect = True


def polygons_to_json():
    json_object = json.dumps(polygons)

    with open(file_name, "w") as outfile:
        outfile.write(json_object)


# draw polygons from json


def json_to_polygons():
    try:
        with open(file_name, 'r') as openfile:
            return json.load(openfile)
    except IOError:
        return []


polygons = json_to_polygons()
# vid = cv2.VideoCapture(0)


def runDetech(rtsp_link):
    global currentPoints
    global polygons
    global detect
    vid = cv2.VideoCapture(rtsp_link)
    while True:

        #     frame = vid.read()

        #     cv2.imshow('cameraaaaa', frame )
        #     key = cv2.waitKey(1)
        #     if key == ord('q'):
        #         break

        # video.stop()
        # cv2.destroyAllWindows()

        ret, frame = vid.read()

        # Ve polygon
        # frame = draw_polygon(frame, points)

        draw_polygon(frame, currentPoints)

        for points in polygons:
            frame = draw_polygon(frame, points)

            if detect:
                frame = model.detect(frame=frame, points=points)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        # Bấm a để nối 2 điểm còn lại của polygons
        elif key == ord('a'):

            if currentPoints:
                currentPoints.append(currentPoints[0])
                polygons.append(currentPoints)
            currentPoints = []
            detect = True

        # Bấm d để xóa mỗi cạnh của polygon
        elif key == ord('d'):

            if currentPoints:
                currentPoints.pop()
            elif polygons:
                polygons.pop()

        # Bấm s để trích polygons thành lưu tọa độ vào json
        elif key == ord('s'):
            polygons_to_json()
            break

        # Hien anh ra man hinh
        cv2.namedWindow("Instrusion Warning", cv2.WINDOW_NORMAL)
        cv2.imshow("Instrusion Warning", frame)

        # cv2.setMouseCallback('Instrusion Warning', handle_left_click, points)
        cv2.setMouseCallback('Instrusion Warning',
                             handle_left_click, currentPoints)

    vid.release()
    cv2.destroyAllWindows()
