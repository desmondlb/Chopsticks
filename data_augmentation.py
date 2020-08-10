import numpy as np
import random
from skimage.util import random_noise
from scipy import ndimage
import cv2
import os


# Perform Data Augmentation
# Operations include rotation, flipping on the vertical axis and adding random noise


class DataAugment:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    # Rotates by a random value between -20 and +20 degrees

    def random_rotation(self, img_to_transform):
        try:
            rotation_degree = random.uniform(-20, 20)

            return ndimage.rotate(img_to_transform, rotation_degree)

        except Exception as ex:
            print(ex)

    # Randomly chooses between salt&pepper noise and gaussian noise which is added to the image

    def add_random_noise(self, img_to_transform):
        try:
            mode = random.choice(['s&p', 'gaussian'])
            noise_img = random_noise(img_to_transform, mode=mode)
            noise_img = np.array(255 * noise_img, dtype=np.uint8)

            return noise_img

        except Exception as ex:
            print(ex)

    # Crops random portion of the image with 65% of the original dimensions

    def random_crop(self, img_to_transform):
        try:
            x = random.randint(0, int(img_to_transform.shape[1] - 0.65 * img_to_transform.shape[1]))
            y = random.randint(0, int(img_to_transform.shape[0] - 0.65 * img_to_transform.shape[0]))
            img_crop = img_to_transform[y:int(y + 0.65 * img_to_transform.shape[0]), x:int(x + 0.65 * img_to_transform.shape[1])]
            return img_crop

        except Exception as ex:
            print(ex)

    # Flips the image on the vertical axis

    def horizontal_flip(self, img_to_transform):
        try:
            return img_to_transform[:, ::-1]

        except Exception as ex:
            print(ex)

    # Following functions iterates through all the directories in the Dataset folder
    # It generates 3 new images for every image in the dataset

    def augment(self):
        try:
            for root, dirs, _ in os.walk(self.dataset_path):
                if len(dirs)==0:
                    dirs.append(os.path.split(dataset_path)[1])
                    root = os.path.split(dataset_path)[0]
                for img_dir in dirs:
                    base_path = os.path.join(root, img_dir)
                    for filename in os.listdir(base_path):
                        if os.path.splitext(filename)[1].lower() == '.jpg':
                            image_path = os.path.join(base_path, filename)
                            img = cv2.imread(image_path, cv2.COLOR_BGR2RGB)

                            path_without_ext = os.path.join(base_path, os.path.splitext(filename)[0])

                            cv2.imwrite(path_without_ext + "_rc.jpg", self.random_crop(img))
                            cv2.imwrite(path_without_ext + "_rot.jpg", self.random_rotation(img))
                            cv2.imwrite(path_without_ext + "_noisy.jpg", self.add_random_noise(img))
                            cv2.imwrite(path_without_ext + "_lrflip.jpg", self.horizontal_flip(img))

        except Exception as ex:
            print(ex)


dataset_path = 'D:\\Projects\\Chopsticks\\Datasets\\HandDetect\\test\\1'
aug = DataAugment(dataset_path)
aug.augment()
