import os
import random

import cv2
import numpy as np
from tqdm import tqdm

class ModelData():
    IMG_SIZE = 50
    CATS = "PetImages/Cat"
    DOGS = "PetImages/Dog"
    TESTING = "PetImages/Testing"
    LABELS = {CATS: 0, DOGS: 1}
    TRAINING_DATAFILE = "PetImages/training_data.npy"
    TESTING_DATAFILE = "PetImages/testing_data.npy"
    training_data = []
    testing_data = []
    training_catcount = 0
    training_dogcount = 0
    testing_catcount = 0
    testing_dogcount = 0

    def __init__(self):
        if (not os.path.isfile(self.TRAINING_DATAFILE) or not os.path.isfile(self.TESTING_DATAFILE)):
            for label in self.LABELS:
                print(f"{label}\n")
                for f in tqdm(os.listdir(label)):
                    if "jpg" in f:
                        try:
                            path = os.path.join(label, f)
                            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                            img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
                            # Randomly take 10% of the images as testing data
                            if(random.randint(0, 100) > 90):
                                # Each element is a tensor with two elements:
                                # elem[0] is the image
                                # elem[1] is a "one-hot" tensor of the classification
                                # "one-hot" means if the image is a cat elem[1] is [1., 0.] and
                                # if the image is a dog then elem [1] is [0., 1.]
                                self.testing_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])
                                if label == self.CATS:
                                    self.testing_catcount += 1
                                elif label == self.DOGS:
                                    self.testing_dogcount += 1
                            else:
                                self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])
                                if label == self.CATS:
                                    self.training_catcount += 1
                                elif label == self.DOGS:
                                    self.training_dogcount += 1
                        except Exception:
                            pass
        
            np.random.shuffle(self.training_data)
            np.save(self.TRAINING_DATAFILE, self.training_data)
            np.save(self.TESTING_DATAFILE, self.testing_data)
            print('Training Cats:', self.training_catcount)
            print('Training Dogs:', self.training_dogcount)
            print('Training Cats:', self.testing_catcount)
            print('Training Dogs:', self.testing_dogcount)

    def get_training_data(self):
        if(len(self.training_data) == 0):
            self.training_data = np.load(self.TRAINING_DATAFILE, allow_pickle=True)
        return self.training_data
    
    def get_testing_data(self):
        if(len(self.testing_data) == 0):
            self.testing_data = np.load(self.TESTING_DATAFILE, allow_pickle=True)
        return self.testing_data
            
