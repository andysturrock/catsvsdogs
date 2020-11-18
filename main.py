import io
import sys
import datetime
import os.path

import cv2
import torch
from cnn import CNN

from model_data import ModelData


# Hold these as constants for now.
# Maybe make them command line params etc later.
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

def train_model():
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
        logfile.write("timestamp,epoch,in_sample,accuracy,loss\n")
        for epoch in range(EPOCHS):
            cnn.train_model(BATCH_SIZE, training_images, training_classifications, logfile, epoch)
            accuracy = cnn.test_model(testing_images, testing_classifications)
            print(f"Accuracy: {accuracy}")

    print(f"Saving trained model as {MODEL_NAME}.pt...")
    torch.save(cnn.state_dict(), f"{MODEL_NAME}.pt")
    print("Done.")


def use_model(state_dict_file):
    print("Creating neural net...")
    cnn = CNN(IMG_SIZE, KERNEL_SIZE, device)
    cnn.load_state_dict(torch.load(state_dict_file))
    cnn.eval()

    path = sys.argv[2]
    if not os.path.isfile(path):
        raise Exception(f"File {path} does not exist")
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise Exception(f"Cannot load file {path}")
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    img_data = torch.Tensor(img).view(-1, IMG_SIZE, IMG_SIZE)
    img_data = img_data / 255.0

    img_data = img_data.view(-1, 1, IMG_SIZE, IMG_SIZE)
    img_data = img_data.to(device)
    result = cnn(img_data)
    if(result[0][0] > result[0][1]):
        print(f"{path} is a cat ({round(float(result[0][0]*100), 2)}% confidence)")
    else:
        print(f"{path} is a dog ({round(float(result[0][1]*100), 2)}% confidence)")

if len(sys.argv) > 2 and os.path.isfile(sys.argv[1]):
    with open(sys.argv[1], 'rb') as state_dict_file:
        bytes_io = io.BytesIO(state_dict_file.read())
        use_model(bytes_io)
else:
    train_model()
