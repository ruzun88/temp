# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 00:54:24 2017

입력: 프로젝트 폴더 내 data/txt 폴더 내에 있는 불량 die 정보
출력: data/img_v3 폴더에 이미지가 생성됨

@author: ruzun
"""

import os
from os import path
import numpy as np
from PIL import Image, ImageOps

# 
path_src = "./data/txt"
out_folder = "img_v3"
img_size = 299

abspath_src = path.abspath(path_src)

file_paths = [path.join(abspath_src, name) for name in os.listdir(path_src) if path.isfile(path.join(abspath_src, name))]
for file in file_paths:
    data = np.genfromtxt(file, delimeter=';', dtype=None)
    coordinates = data[data[:,4]==b'W'][:,2:4].astype(np.uint8)
    coordinates_list = []
    for coordinate in coordinates:
        coordinates_list.append(list(coordinate))
    cluster_coord = []
    for coordinate in coordinates_list:
        near_pt_cnt = 0
        cor_x, cor_y = coordinate
        if[cor_x - 1, cor_y -1] in coordinates_list:
            near_pt_cnt +=1
        if [cor_x -1, cor_y] in coordinates_list:
            near_pt_cnt += 1
        if [cor_x-1, cor_y+1] in coordinates_list:
            near_pt_cnt +-1
        if [cor_x, cor_y -1] in coordinates_list:
            near_pt_cnt += 1
        if [cor_x, cor_y +1] in coordinates_list:
            near_pt_cnt += 1
        if [cor_x +1, cor_y -1] in coordinates_list:
            near_pt_cnt += 1
        if [cor_x + 1, cor_y + 1] in coordinates_list:
            near_pt_cnt += 1

        if near_pt_cnt > 1:
            cluster_coord.append(coordinate)

    array = np.zeros(shape=(50, 70), dtype = np.uint8)
    cluster_coord = np.array(cluster_coord)
    array[cluster_coord[:,1], cluster_coord[:,0]] = 255
    img = Image.fromarray(array).crop((10,10,62,42)).resize((img_size,img_size))
    img = ImageOps.invert(img)
    img_filename = file.replace(path.sep+'txt'+path.sep, path.sep+out_folder+path.sep)[:-4]+'.png'
    img.save(img_filename)
    lot_id = file.split(path.sep)[-1].split('.')[0]
    print(lot_id, '-- image generated')