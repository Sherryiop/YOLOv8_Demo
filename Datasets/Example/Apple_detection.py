from ultralytics import YOLO
import cv2
import numpy as np
import math

import argparse
from collections import defaultdict
from pathlib import Path

from shapely.geometry import Polygon
from shapely.geometry.point import Point

from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors
import time

def box_center(left, top, right, bottom):
    width = right - left
    height = bottom - top
    center_x = left + int((right-left)/2)
    center_y = top + int((bottom-top)/2)
    
    return center_x, center_y

#===========================================================#
# 模型和影片路徑設定
#===========================================================#
model_path = r'path\to\runs\detect\train\weights\best.pt' # YOLO model path
source = r'path\to\Datasets\Example\images\train\apple.jpg' # input path
output_path = r'path\to\Datasets\Example\output.jpg' # picture output path
model = YOLO(model_path)
#===========================================================#

region_thickness = 5 #區域框線寬度
Apple_x = 0
Apple_y = 0
count_Apple = 0
names = model.model.names

results = model(source)
            
for result in results:
    frame = result.plot()
    for i, box in enumerate(result.boxes):
        left, top, right, bottom = np.array(box.xyxy.cpu(), dtype=np.int32).squeeze()
        center_x, center_y = box_center(left, top, right, bottom)  # 每個物件框的中心點

        object_name = result.names[box.cls.item()]
        if  object_name == 'Apple': 
            Apple_x, Apple_y = center_x, center_y
            count_Apple += 1
        cv2.putText(frame, str(count_Apple), (Apple_x, Apple_y), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (229,187,70),2)         


cv2.imwrite(output_path, frame)
cv2.imshow('Image Detection', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()