import os
import random

import cv2
import numpy as np
from tqdm import tqdm


class ModelData:
    CATS = "PetImages/Cat"
    DOGS = "PetImages/Dog"
    # TESTING = "PetImages/Testing"
    LABELS = {CATS: 0, DOGS: 1}
    TRAINING_DATAFILE = "PetImages/training_data.npy"
    TESTING_DATAFILE = "PetImages/testing_data.npy"
    training_data = []
    testing_data = []
    training_catcount = 0
    training_dogcount = 0
    testing_catcount = 0
    testing_dogcount = 0

    def __init__(self, img_size):
        # If both training and testing files exist already then just exit
        if os.path.isfile(self.TRAINING_DATAFILE) and os.path.isfile(
            self.TESTING_DATAFILE
        ):
            return

        # Use a "one-hot" tensor for the classification
        # "one-hot" means if the image is a cat then the tensor is [1., 0.]
        # and if the image is a dog then it's [0., 1.]
        one_hot = {self.CATS: [1.0, 0.0], self.DOGS: [0.0, 1.0]}

        for label in self.LABELS:
            for f in tqdm(os.listdir(label)):
                if "jpg" in f:
                    path = os.path.join(label, f)
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    # imread returns None if it can't read the image so just ignore this one
                    if img is None:
                        continue
                    img = cv2.resize(img, (img_size, img_size))

                    # Take a random 10% of the images as testing data
                    if random.randint(0, 100) > 90:
                        # Each element is a tensor with two elements:
                        # elem[0] is the image
                        # elem[1] is a the classification as a one-hot vector
                        self.testing_data.append([np.array(img), one_hot[label]])
                        if label == self.CATS:
                            self.testing_catcount += 1
                        elif label == self.DOGS:
                            self.testing_dogcount += 1
                    else:
                        self.training_data.append([np.array(img), one_hot[label]])
                        if label == self.CATS:
                            self.training_catcount += 1
                        elif label == self.DOGS:
                            self.training_dogcount += 1

        np.random.shuffle(self.training_data)
        np.save(self.TRAINING_DATAFILE, self.training_data)
        np.save(self.TESTING_DATAFILE, self.testing_data)
        print("Training Cats:", self.training_catcount)
        print("Training Dogs:", self.training_dogcount)
        print("Testing Cats:", self.testing_catcount)
        print("Testing Dogs:", self.testing_dogcount)

    def get_training_data(self):
        if len(self.training_data) == 0:
            self.training_data = np.load(self.TRAINING_DATAFILE, allow_pickle=True)
        return self.training_data

    def get_testing_data(self):
        if len(self.testing_data) == 0:
            self.testing_data = np.load(self.TESTING_DATAFILE, allow_pickle=True)
        return self.testing_data
