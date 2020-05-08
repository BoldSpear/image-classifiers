#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:42:22 2020

@author: swilson
"""
import json
import boto3
import numpy as np
import base64
import io
import cv2

import os
import collections


def pic_val_count(img_name):
    """
    the function counts colors (R,G,B) of input image, and returns with frequency
    < Arguments >
    * img_nam: image file name, e.g.) 'image.png'
    """
    pic = cv2.imread(img_name)
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)

    reshaped_pic = np.reshape(pic, (pic.shape[0]*pic.shape[1], 3))
    reshaped_pic = reshaped_pic.tolist()
    reshaped_pic = [tuple(pixel) for pixel in reshaped_pic]
    
    col_count = []
    for i in set(reshaped_pic):
        (col_val, num_pic)  = i,  reshaped_pic.count(i)
        col_count.append((col_val, num_pic))        
    return col_count


def classify_feature_image(input_img, feature_colors, pix_cutoff=50):
    """
    the function detects color of interest from input image
    < Arguments >
    * input_img: image file name, e.g.) 'image.png'
    * feature_colors: a list of featured color obtained from "dominant_color_set()"
    * pix_cutoff: the threshold number of featured pixel to be considered 'positive' image
    """
    result = 'negative'
    for pic_val, num in pic_val_count(input_img):
        for min_rgb, max_rgb in feature_colors:
            if (((min_rgb[0] <= pic_val[0] <= max_rgb[0])
            &(min_rgb[1] <= pic_val[1] <= max_rgb[1])
            &(min_rgb[2] <= pic_val[2] <= max_rgb[2])) & (num > pix_cutoff)):
                result = "positive"
    return result


def classify_feature_image(input_img, pix_cutoff=50):
    result = 0
    for pic_val, num in pic_val_count(input_img):
        if (min_R <= pic_val[0] <= max_R):
            &(min_G <= pic_val[1] <= max_G)
            &(min_B <= pic_val[2] <= max_B)
            &(num > pix_cutoff):
                result = 1
    return result




###########################
# Test
###########################    
#--- load featured color values 
THIS_FOLDER = os.getcwd()
model_file = os.path.join(THIS_FOLDER, 'landuse_construction.txt')

f = open(model_file, "r")
col_vals = f.read().splitlines()
f.close()

col_vals = [int(val) for val in col_vals]

#--- pixel values of the map feature
min_R, max_R = col_vals[0], col_vals[1] 
min_G, max_G = col_vals[2], col_vals[3]  
min_B, max_B = col_vals[4], col_vals[5] 


# positive
classify_feature_image('./COLOR_construction.png', pix_cutoff=50)
# negative
classify_feature_image('./COLOR_not_construction.png', pix_cutoff=50)

