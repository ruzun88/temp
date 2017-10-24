# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 00:59:43 2017
입력 : 해당 폴더 내에 있는 그림파일
출력 : 스무딩 된 그림 파일
@author: ruzun
"""

import cv2
import numpy as np
import os
from os import path

default_directory = 'd:/Personal_workspace/OpenCV/TCL_WF_MAP/'
os.chdir(default_directory)
imgs = [path.join(default_directory, name) for name in os.listdir(default_directory) if path.isfile(path.join(default_directory, name))]

for img_file in imgs:
    img = cv2.imread(img_file, 0)
    kernel = np.ones((5,5), np.uint8)
    rows, cols = img.shape[:2]

    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    
    # 블러링
    kernel_10x10 = np.ones((10,10), np.float32) / 100.0
    cv2.imshow('Original', img)
    
    output = cv2.filter2D(img, -1, kernel_10x10)
    cv2.imshow('10x10 filter', output)
    
    output = cv2.erode(output, kernel, iterations = 1)
    output = cv2.dilate(output, kernel, iterations=2)
    img_test = cv2.erode(output, kernel, iterations=1)
    cv2.imshow('before Thresholding', img_test)
    ret, thr1 = cv2.threshold(img_test, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('test', thr1)
    cv2.imwrite('./output_skeleton/' + img_file.split('/')[-1], thr1)
    
    thr1 = cv2.filter2D(thr1, -1, kernel_10x10)
    ret, thr1 = cv2. threshold(thr1, 200, 255, cv2.THRESH_BINARY)
    
    cv2.imwrite('./output2/' + img_file.split('/')[-1], thr1)
    cv2.imshow('test2', thr1)
    
    thr1 = 255 - thr1
    while(not done):
        eroded = cv2.erode(thr1, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(thr1, temp)
        skel = cv2.bitwise_or(skel, temp)
        thr1 = eroded.copy()
    
        zeros = size - cv2.countNonZero(thr1)
        if zeros==size:
            done = True
    
    skel = 255 - skel
    cv2.imwrite('./output_skeleton/' + img_file.split('/')[-1], skel)
    cv2.imshow('skeleton', skel)
    
cv2.waitKey(0)
cv2.destroyAllWindows()