import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import SGD
from classification_models.tfkeras import Classifiers


def get_train_test(train_path, test_path, target):
    trdata = ImageDataGenerator()
    traindata = trdata.flow_from_directory(directory=train_path, target_size=(target, target), shuffle=True)

    tsdata = ImageDataGenerator()
    testdata = tsdata.flow_from_directory(directory=test_path, target_size=(224, 224), shuffle=True)

    return traindata, testdata


def add_custom_layers(base_model, dense_layers, activation, base_trainable):
    if not base_trainable:
        for layers in base_model.layers:
            layers.trainable = False
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = Dense(dense_layers[0])(x)
    x = Dense(dense_layers[1])(x)
    output = Dense(2, activation=activation)(x)
    model = Model(base_model.input, output)
    return model


def train(model, traindata, testdata):
    checkpoint = ModelCheckpoint("Resnet18_1.h5", monitor='val_accuracy', verbose=1,
                                 save_best_only=True, save_weights_only=False, mode='auto', save_freq='epoch')
    early = EarlyStopping(monitor='val_accuracy', min_delta=0, patience=30, verbose=1, mode='auto')
    model.fit_generator(generator=traindata, steps_per_epoch=5, epochs=100,
                        validation_data=testdata, validation_steps=1, callbacks=[checkpoint, early])
    model.save_weights("Resnet18_1.h5.h5")


def load_base_model():
    ResNet18, preprocess_input = Classifiers.get('resnet18')
    base_model = ResNet18(input_shape=(224, 224, 3), weights='imagenet', include_top=False)
    return base_model


train_path = "D:/Projects/Chopsticks/Datasets/HandDetect/train"
test_path = "D:/Projects/Chopsticks/Datasets/HandDetect/test"
image_inp_size = 224
traindata, testdata = get_train_test(train_path, test_path, image_inp_size)

base_model = load_base_model()
dense_layers = [1024, 256]
model = add_custom_layers(base_model, dense_layers, activation='softmax', base_trainable = False)
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])
train(model, traindata, testdata)
