import numpy as np
import os

from keras.models import Model
from keras.layers import Dense, Dropout
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
# from utils.score_utils import mean_score, std_score
from skimage import io
import csv
import cv2

from keras.models import load_model  
from keras.preprocessing import image

#filename = 'input.csv'
filename = 'input.txt'
csvFile = open('result.csv', 'w')
f=open(filename)
writer = csv.writer(csvFile)
#reader = csv.reader(f)
lines = f.readlines()
# base_model = InceptionResNetV2(input_shape=(None, None, 3), include_top=False, pooling='avg', weights=None)
# x = Dropout(0.75)(base_model.output)
# x = Dense(10, activation='softmax')(x)
# model = Model(base_model.input, x)
# model.load_weights('weights/inception_resnet_weights.h5')
model = load_model("./model/model.hdf5")
writer.writerow(['id', 'prediction'])
#for line in list(reader)[1:200]:
count = 0
right = 0
for line in lines:
    #id,url=line
    id,url=line.strip('\n').split('\t')
    if url[-3:]=='png':
        url=url[:-3] + 'jpg'
    if url=='NULL' or url[-3:]!='jpg':
        writer.writerow([id, '-1'])
        continue
    img=io.imread(url)
    img=cv2.resize(img,(224,224))
    x = img_to_array(img)
    if x.shape[0]<100 or x.shape[1]<100:
        writer.writerow([id, '-1'])
        continue
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    score = model.predict(x, batch_size=64, verbose=0)[0,0]
    writer.writerow([id, score])
    # print(id,score)
    count += 1
    if (score - 0) > 0.1:
        right += 1
        print (id, score)
print (count, right)
csvFile.close()
f.close()
