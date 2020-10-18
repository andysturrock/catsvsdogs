import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from model_data import ModelData
from cnn import CNN



if torch.cuda.is_available():
    device = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc. 
    print("Running on the GPU")
else:
    device = torch.device("cpu")
    print("Running on the CPU")

model_data = ModelData()
training_data = model_data.get_training_data()

cnn = CNN(device)
batch_size = 100
epochs = 3

X = torch.Tensor([i[0] for i in training_data]).view(-1, 50, 50)
X = X/255.0
y = torch.Tensor([i[1] for i in training_data])

cnn.train(epochs, batch_size, torch.Tensor([i[0] for i in training_data]).view(-1, 50, 50), torch.Tensor([i[1] for i in training_data]))