from yolov8 import YOLOv8

yolov8 = YOLOv8()
yolov8.load("ok/eye0001.png")

reults = yolov8.detect("ok/eye0001.png")