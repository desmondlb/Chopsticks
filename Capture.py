import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json

videoCaptureObject = cv2.VideoCapture(0)
X1 = [20, 340, 20, 340]
Y1 = [20, 20, 260, 260]
X2 = [300, 620, 300, 620]
Y2 = [220, 220, 460, 460]

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("Resnet18_1.h5")
print("Loaded model from disk")

while True:
    ret,frame = videoCaptureObject.read()
    frame = cv2.flip(frame, 1)

    for i in range(4):
        cv2.rectangle(frame, (X1[i], Y1[i]), (X2[i], Y2[i]), (255, 0, 0), 2)

    cv2.imshow('Capturing Video',frame)

    cpul = frame[Y1[0]: Y2[0], X1[0]: X2[0]]
    cv2.imshow('1st', cpul)
    # cpur = frame[Y1[1]: Y2[1], X1[1]: X2[1]]
    # cv2.imshow('2nd', cpur)
    # pll = frame[Y1[2]: Y2[2], X1[2]: X2[2]]
    # cv2.imshow('3rd', pll)
    # plr = frame[Y1[3]: Y2[3], X1[3]: X2[3]]
    # cv2.imshow('4th', plr)

    # img = image.load_img(cpul, target_size=(224, 224))
    cpul1 = cv2.resize(cpul, (224, 224))
    img = np.asarray(cpul1)
    img = np.expand_dims(img, axis=0)
    print(img.shape)

    output = loaded_model.predict(img)

    if output[0][0] < output[0][1]:
        print("hand")
        cv2.rectangle(frame, (X1[0], Y1[0]), (X2[0], Y2[0]), (255, 255, 0), 5)
    else:
        continue

    if cv2.waitKey(1) & 0xFF == ord('q'):
        videoCaptureObject.release()
        cv2.destroyAllWindows()