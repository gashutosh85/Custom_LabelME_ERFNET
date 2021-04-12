import sys
from bs4 import BeautifulSoup 
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import scipy.io
import scipy.io as sio


color_dict={'unlabeled': (0, 0, 0), 'ego vehicle': (0, 0, 0), 'rectification border': (0, 0, 0), 'out of roi': (0, 0, 0), 'static': (0, 0, 0), 'dynamic': (111, 74, 0), 'ground': (81, 0, 81), 'road': (128, 64, 128), 'sidewalk': (244, 35, 232), 'parking': (250, 170, 160), 'rail track': (230, 150, 140), 'building': (70, 70, 70), 'wall': (102, 102, 156), 'fence': (190, 153, 153), 'guard rail': (180, 165, 180), 'bridge': (150, 100, 100), 'tunnel': (150, 120, 90), 'pole': (153, 153, 153), 'polegroup': (153, 153, 153), 'traffic light': (250, 170, 30), 'traffic sign': (220, 220, 0), 'vegetation': (107, 142, 35), 'terrain': (152, 251, 152), 'sky': (70, 130, 180), 'person': (220, 20, 60), 'rider': (255, 0, 0), 'car': (0, 0, 142), 'truck': (0, 0, 70), 'bus': (0, 60, 100), 'caravan': (0, 0, 90), 'trailer': (0, 0, 110), 'train': (0, 80, 100), 'motorcycle': (0, 0, 230), 'bicycle': (119, 11, 32), 'license plate': (0, 0, 142)}

color_ids = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (111, 74, 0), (81, 0, 81), (128, 64, 128), (244, 35, 232), (250, 170, 160), (230, 150, 140), (70, 70, 70), (102, 102, 156), (190, 153, 153), (180, 165, 180), (150, 100, 100), (150, 120, 90), (153, 153, 153), (153, 153, 153), (250, 170, 30), (220, 220, 0), (107, 142, 35), (152, 251, 152), (70, 130, 180), (220, 20, 60), (255, 0, 0), (0, 0, 142), (0, 0, 70), (0, 60, 100), (0, 0, 90), (0, 0, 110), (0, 80, 100), (0, 0, 230), (119, 11, 32), (0, 0, 142)]

label_id = [255, 255, 255, 255, 255, 255, 255, 0, 1, 255, 255, 2, 3, 4, 255, 255, 255, 5, 255, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 255, 255, 16, 17, 18, -1]

folder_name = sys.argv[1]
file_name = sys.argv[2]


# file_name = 'img1.png'
with open(os.path.join('../../Annotations/overlayed_images_for_scribbles',file_name[:-4]+'.xml'), 'r') as f: 
    data = f.read() 
original_prediction = cv2.imread(os.path.join('../../Images/original_predictions',file_name))
original_prediction = cv2.cvtColor(original_prediction, cv2.COLOR_BGR2RGB)


Bs_data = BeautifulSoup(data, "lxml") 

mat_mask  = np.zeros(original_prediction.shape[0:2],dtype=int)


objects = Bs_data.find_all('object') 
for obj in objects:
    object_id = str(obj.find_all('name'))[7:-8]
    scribble_id = str(obj.find_all('scribble_name')[0])[15:-16]
    scribble_mask = cv2.imread(os.path.join('../../Scribbles/overlayed_images_for_scribbles',scribble_id))
    scribble_mask = cv2.cvtColor(scribble_mask, cv2.COLOR_BGR2RGB)
    original_prediction[(scribble_mask[:, :, 0:3] == [0,0,255]).all(2)]=color_dict[object_id]
    mat_mask[(scribble_mask[:, :, 0:3] == [0,0,255]).all(2)] = 1


original_prediction_copy = cv2.cvtColor(original_prediction, cv2.COLOR_BGR2RGB)
cv2.imwrite(os.path.join('../../Images/corrected_prediction',file_name), original_prediction_copy) 
scipy.io.savemat('/var/www/html/work/work/erfnet_pytorch/train/mask.mat', {'I1': mat_mask})
# print("prediction corrected using scribble inputs")

##convert original image to trainLabelIDs

# original_prediction = cv2.cvtColor(original_prediction, cv2.COLOR_BGR2RGB)
for index,color in enumerate(color_ids):
    original_prediction[np.all(original_prediction == color, axis=-1)] = label_id[index]    
    
original_prediction = cv2.cvtColor(original_prediction, cv2.COLOR_RGB2GRAY)
cv2.imwrite(os.path.join('../../Images/TrainImgIds',file_name), original_prediction)        
# print("color image converted to trainLabelIDs")