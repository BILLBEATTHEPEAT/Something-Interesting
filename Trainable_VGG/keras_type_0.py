# Trainable VGG16 with Keras
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input


from  keras.layers.core  import Dense, Flatten, Dropout
from keras.models import Model

from keras import optimizers

from keras import initializers
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import multi_gpu_model

input_shape = (224,224,3)


base_model = VGG16(include_top = False, weights = 'imagenet', input_shape = input_shape)
for layer in base_model.layers:
    layer.trainable = False
model = Flatten(name='Flatten',)(base_model.output)
model = Dropout(0.2)(model)
model = Dense(4096, kernel_initializer='random_uniform',)(model)
model = Dense(1024, kernel_initializer='random_uniform')(model)
model = Dense(2, activation = 'sigmoid')(model)
final_model = Model(inputs=base_model.input, outputs = model, name = 'Modified_VGG16')

# sgd = SGD(lr=0.05, decay=1e-5)
adam = optimizers.Adam(lr=0.00001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
# final_model.compile(loss='binary_crossentropy',  
#               optimizer=adam,  
#               metrics=['accuracy'])

print (final_model.summary())

parallel_model = multi_gpu_model(final_model, gpus=4)
parallel_model.compile(loss='binary_crossentropy',
                       optimizer=adam,metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True
    )

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    directory = './dataset/train/',
    target_size = input_shape[:-1],
    color_mode = 'rgb',
    classes = None,
    class_mode = 'categorical',
    batch_size = 512,
    shuffle = True)

test_generator = test_datagen.flow_from_directory(
    directory = './dataset/test/',
    target_size = input_shape[:-1],
    batch_size = 512,
    class_mode = 'categorical')

check = ModelCheckpoint(filepath='/home/bipkg/workspace/SensitivePic/keras/checkpoint/weights.hdf5', 
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

parallel_model.fit_generator(
    generator = train_generator,
    epochs = 100,
    verbose = 1,
    steps_per_epoch=2000,
    validation_data = test_generator,
    shuffle = True,
    # callbacks = [check, stop]
    callbacks = [check]
    )

final_model.save_weights('/home/bipkg/workspace/SensitivePic/keras/model/fine_tuned_net_weight_0.h5')
final_model.save('/home/bipkg/workspace/SensitivePic/keras/model/fine_tuned_net_model_0.h5')
print ("model saved")

# parallel_model.fit(x, y, epochs=20, batch_size=256)
