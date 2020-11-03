import datetime

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from cnn import CNN
import matplotlib.pyplot as plt

from model_data import ModelData


IMG_SIZE = 50
KERNEL_SIZE = 5
BATCH_SIZE = 100
EPOCHS = 5

if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print("Running on the GPU")
else:
    device = torch.device("cpu")
    print("Running on the CPU")

print("Loading training and test data...")
model_data = ModelData(IMG_SIZE)
training_data = model_data.get_training_data()
testing_data = model_data.get_testing_data()

print("Scaling training data...")
training_images = torch.Tensor([i[0] for i in training_data]).view(-1, IMG_SIZE, IMG_SIZE)
# The images are greyscale values between 0 and 255, whereas we need them
# to be between 0 and 1 (as floats) so scale them.
training_images = training_images / 255.0
training_classifications = torch.Tensor([i[1] for i in training_data])

print("Scaling testing data...")
testing_images = torch.Tensor([i[0] for i in testing_data]).view(-1, IMG_SIZE, IMG_SIZE)
# See above
testing_images = testing_images / 255.0
testing_classifications = torch.Tensor([i[1] for i in testing_data])

print("Creating neural net...")
cnn = CNN(IMG_SIZE, KERNEL_SIZE, device)

print("Training model...")
now = datetime.datetime.now()
nowStr = now.strftime("%Y-%m-%d_%H.%M.%S")
MODEL_NAME = f"model-{nowStr}"
with open(f"{MODEL_NAME}.csv", "a") as logfile:
    # header row
    logfile.write(f"timestamp,epoch,in_sample,accuracy,loss\n")
    for epoch in range(EPOCHS):
        cnn.train(BATCH_SIZE, training_images, training_classifications, logfile, epoch)
        cnn.test(testing_images, testing_classifications)