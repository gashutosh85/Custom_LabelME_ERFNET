import sys
from bs4 import BeautifulSoup 
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os

folder_name = sys.argv[1]
file_name = sys.argv[2]
original_img = cv2.imread(os.path.join("../../Images/"+str(folder_name),file_name))

original_prediction = cv2.imread(os.path.join('../../Images/original_predictions',file_name))
original_img = cv2.resize(original_img, (original_prediction.shape[:-1][1],original_prediction.shape[:-1][0]))
added_image = cv2.addWeighted(original_img,0.6,original_prediction,0.4,0)
cv2.imwrite(os.path.join('../../Images/overlayed_images_for_scribbles',file_name), added_image)
cv2.imwrite(os.path.join('../../Images/original_images',file_name), original_img)
# print("overlaying images to load into tool for better visualization")