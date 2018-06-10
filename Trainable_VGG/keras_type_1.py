# Trainable VGG16 with Keras
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

import numpy as np
import os


from  keras.layers.core  import Dense, Flatten, Dropout
from keras.models import Model
from keras.utils.np_utils import to_categorical

from keras import optimizers

from keras import initializers
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import multi_gpu_model

from sklearn import preprocessing
scaler = preprocessing.StandardScaler()

input_shape = (224,224,3)


# train_datagen = ImageDataGenerator(
#     rescale=1. / 255,
# #     shear_range=0.2,
# #     zoom_range=0.2,
# #     horizontal_flip=True
#     )

# test_datagen = ImageDataGenerator(rescale=1. / 255)

# train_generator = train_datagen.flow_from_directory(
#     directory = './dataset/train/',
#     target_size = input_shape[:-1],
#     color_mode = 'rgb',
#     classes = None,
#     class_mode = 'categorical',
#     batch_size = 512,
#     shuffle = True)

# test_generator = test_datagen.flow_from_directory(
#     directory = './dataset/test/',
#     target_size = input_shape[:-1],
#     batch_size = 512,
#     class_mode = 'categorical')
train_img_array = np.array([])
train_label_array = np.array([])
dir_path = './dataset/train/'

print ("data loading")
for label in os.listdir(dir_path):
    img_path = dir_path + label + '/'
    index = 0
    for filename in os.listdir(img_path):
        index += 1
        print(label, index)
        img = image.load_img(img_path+filename, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        train_img_array = np.append(train_img_array,x)
        train_label_array = np.append(train_label_array,int(label))

test_img_array = np.array([])
test_label_array = np.array([])
dir_path = './dataset/test/'

for label in os.listdir(dir_path):
    img_path = dir_path + label + '/'
    
    for filename in os.listdir(img_path):

        img = image.load_img(img_path+filename, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        test_img_array = np.append(test_img_array,x)
        test_label_array = np.append(test_label_array,int(label))

# scaler.fit(train_img_array)
train_img_array = train_img_array.reshape(-1, 224, 224, 3)
test_img_array = test_img_array.reshape(-1, 224, 224, 3)
train_label_array = to_categorical(train_label_array, num_classes = 2)
test_label_array = to_categorical(test_label_array, num_classes = 2)

print (train_img_array.shape, test_img_array.shape, train_label_array.shape, test_label_array.shape)



base_model = VGG16(include_top = True, weights = None, input_shape = input_shape, classes = 2)
for layer in base_model.layers[:-1]:
    layer.trainable = False
# model = Flatten(name='Flatten',)(base_model.output)
# model = Dropout(0.2)(model)
# model = Dense(4096, kernel_initializer='random_uniform',)(model)
# model = Dense(1024, kernel_initializer='random_uniform')(model)
# model = Dense(2, activation = 'sigmoid')(model)
# final_model = Model(inputs=base_model.input, outputs = model, name = 'Modified_VGG16')
print ("Model loaded")

bse_model.layers[-1].name = 'pred'
base_model.layers[-1].kernel_initializer = initializers.glorot_normal()
base_model.load_weights('./vgg16_weights_tf_dim_ordering_tf_kernels.h5', by_name = True)


sgd = SGD(lr=0.01, decay=1e-4, momentum=0.9, nesterov=True)
# adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
# base_model.compile(loss='binary_crossentropy',  
#               optimizer=sgd,  
#               metrics=['accuracy'])

print (base_model.summary())

parallel_model = multi_gpu_model(base_model, gpus=4)
parallel_model.compile(loss='binary_crossentropy',
                       optimizer=sgd,
                       metrics=['accuracy'])

check = ModelCheckpoint(filepath='./checkpoint/weights.hdf5', 
                monitor='val_loss', 
                verbose=0, 
                save_best_only=True, 
                save_weights_only=False, 
                mode='auto', 
                period=1)

stop = EarlyStopping(monitor='val_loss',
              min_delta=0, 
              patience=3, 
              verbose=0, 
              mode='auto')

print ("loading Complete")
parallel_model.fit(train_img_array, train_label_array, batch_size = 128, epochs = 100000, validation_split = 0.1)

# parallel_model.fit_generator(
#     generator = train_generator,
#     epochs = 100,
#     verbose = 1,
#     steps_per_epoch=100,
#     validation_data = test_generator,
#     shuffle = True,
#     # callbacks = [check, stop]
#     callbacks = [check]
#     )

final_model.save_weights('./model/fine_tuned_net_weight_0.h5')
final_model.save('./model/fine_tuned_net_model_0.h5')
print ("model saved")

# parallel_model.fit(x, y, epochs=20, batch_size=256)
