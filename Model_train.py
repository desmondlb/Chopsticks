import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import SGD, Adam
from classification_models.tfkeras import Classifiers


def get_train_test(train_path, test_path, target):
    trdata = ImageDataGenerator()
    traindata = trdata.flow_from_directory(directory=train_path, target_size=(target, target), shuffle=True)

    tsdata = ImageDataGenerator()
    testdata = tsdata.flow_from_directory(directory=test_path, target_size=(target, target), shuffle=True)

    return traindata, testdata


def add_custom_layers(base_model, dense_layers, activation, base_trainable):
    if not base_trainable:
        for layers in base_model.layers:
            layers.trainable = False
    x = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = Dense(dense_layers[0])(x)
    x = Dense(dense_layers[1])(x)
    x = Dense(dense_layers[2])(x)
    x = Dense(dense_layers[3])(x)
    output = Dense(4, activation=activation)(x)
    model = Model(base_model.input, output)
    return model


def train(model, traindata, testdata):
    checkpoint1 = ModelCheckpoint("Resnet50.h5", monitor='categorical_accuracy', verbose=1,
                                 save_best_only=True, save_weights_only=False, mode='auto', save_freq='epoch')
    checkpoint2 = ModelCheckpoint("Resnet50.h5", monitor='val_categorical_accuracy', verbose=1,
                                 save_best_only=True, save_weights_only=False, mode='auto', save_freq='epoch')
    early = EarlyStopping(monitor='categorical_accuracy', min_delta=0, patience=30, verbose=1, mode='auto')
    model.fit(traindata, steps_per_epoch=4, epochs=100,
              validation_data=testdata, validation_steps=1, callbacks=[checkpoint1, checkpoint2, early])
    model.save_weights("Resnet50.h5")
    model_json = model.to_json()
    with open("R50_model.json", "w") as json_file:
        json_file.write(model_json)


def load_base_model():
    ResNet50, preprocess_input = Classifiers.get('resnet50')
    base_model = ResNet50(input_shape=(224, 224, 3), weights='imagenet', include_top=False)
    return base_model


train_path = "D:/Projects/Chopsticks/Datasets/new2/train"
test_path = "D:/Projects/Chopsticks/Datasets/new2/test"
image_inp_size = 224
traindata, testdata = get_train_test(train_path, test_path, image_inp_size)

base_model = load_base_model()
dense_layers = [4096, 2048, 1024, 256]
model = add_custom_layers(base_model, dense_layers, activation='softmax', base_trainable=False)
model.compile(optimizer=Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08), loss='categorical_crossentropy', metrics=['categorical_accuracy'])
train(model, traindata, testdata)
