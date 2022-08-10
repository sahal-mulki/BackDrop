import pyvirtualcam
import numpy as np
from PIL import Image
import cv2
import time
import mediapipe as mp

f = open("proc_run.txt", "w")
f.write("true")
class SelfiSegmentation():

    def __init__(self, model=1):
        """
        :param model: model type 0 or 1. 0 is general 1 is landscape(faster)
        """
        self.model = model
        self.mpDraw = mp.solutions.drawing_utils
        self.mpSelfieSegmentation = mp.solutions.selfie_segmentation
        self.selfieSegmentation = self.mpSelfieSegmentation.SelfieSegmentation(self.model)

    def removeBG(self, img, imgBg=cv2.imread("bg_default.png"), threshold=0.9):
        """

        :param img: image to remove background from
        :param imgBg: BackGround Image
        :param threshold: higher = more cut, lower = less cut
        :return:
        """
        #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.selfieSegmentation.process(img)
        binary_mask = results.segmentation_mask > 0.9
        binary_mask_3 = np.dstack((binary_mask,binary_mask,binary_mask))
        imgBg = cv2.resize(imgBg, dsize=(width, height), interpolation=cv2.INTER_CUBIC)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) > threshold
        try:
            imgOut = np.where(condition, img, imgBg)
        except:
            np.zeroes(3)
        return imgOut

x = 0

try:
    imgBg2 = cv2.imread(r'background.png')
except:
    imgBg2 = cv2.imread('bg_default.png')
    imgBg2 = cv2.cvtColor(imgBg, cv2.COLOR_BGR2RGB)

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
detector = SelfiSegmentation()

width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

with pyvirtualcam.Camera(width=width, height=height, fps=20) as cam:
    print(f'Using virtual camera: {cam.device}')
    frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
    print("starting censoring")
    while True:

        x = x + 1
                
        ret, frame = video_capture.read()

        f = open("segmentation.txt", "r")
            
        if f.read() == "true":
            print("ye")
            try:
                frame = detector.removeBG(frame, imgBg=imgBg2, threshold=0.5)
            except:
                frame = detector.removeBG(frame, threshold=0.5)
            frame = cv2.resize(frame.astype(np.uint8), dsize=(width, height), interpolation=cv2.INTER_CUBIC)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            print("ne")
            frame = cv2.resize(frame.astype(np.uint8), dsize=(width, height), interpolation=cv2.INTER_CUBIC)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        f.close()

        f = open("segmentation.txt", "r")
            
        cam.send(frame)
                
        f.close()
            
        
        
        if x % 5 == 0:

            f = open("preview_condition.txt", "r")
            
            if f.read() == "save":

                cv2.imwrite("preview.png", frame)
                
            f.close()
        if x % 5 == 0:
            try:
                imgBg2 = cv2.imread(r'background.png')
            except:
                imgBg2 = cv2.imread('bg_default.png')
                imgBg2 = cv2.cvtColor(imgBg, cv2.COLOR_BGR2RGB)




        cam.sleep_until_next_frame()
        
