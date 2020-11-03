import time

from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class CNN(nn.Module):
    def __init__(self, img_size, kernel_size, device):
        super().__init__()
        self.img_size = img_size
        self.device = device

        # Layer 1 takes in 1 channel and returns 32 channels, with "kernel" (like a window on the image) of kernel_size
        self.conv1 = nn.Conv2d(1, 32, kernel_size)
        # Layer 2 takes in 32 channels (from layer 1) and returns 64 channels, with kernel of kernel_size
        self.conv2 = nn.Conv2d(32, 64, kernel_size)
        # Layer 3 takes in 64 channels (from layer 2) and returns 128 channels, with kernel of kernel_size
        self.conv3 = nn.Conv2d(64, 128, kernel_size)

        # We need to work out the shape of the input features for the first Linear layer
        # So stick some random data through the convolutional layers and use that to calculate it.
        x = torch.randn(self.img_size, self.img_size).view(-1, 1, self.img_size, self.img_size)
        self._to_linear = None
        self.convs(x)

        # So now linear layer 1 takes in size "_to_linear" input sample and returns output sample size 512
        self.fc1 = nn.Linear(self._to_linear, 512)
        # Linear layer 2 takes the sample size 512 and cuts it down to 2.
        self.fc2 = nn.Linear(512, 2)

        # Use the Adam algorithm for optimisation.  See docs.
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        # Use Mean Squares Error for the loss function
        self.loss_function = nn.MSELoss()

    # Run the convolutional layers
    def convs(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2,2))

        if self._to_linear is None:
            self._to_linear = x[0].shape[0] * x[0].shape[1] * x[0].shape[2]
        return x

    # Do the computation.  Inherited from base class.
    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, self._to_linear)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

    # Train the model
    # train_X is the input images
    # train_y is the input image classification in one-hot format: [1, 0] for cat, [0, 1] for dog
    # logfile should be already opened for append.  Can be a file, or STDIN etc.
    # Epoch is optional and can be used to show in the logfile how many times this function has been called.
    def train(self, batch_size, train_X, train_y, logfile, epoch=1):
        for i in tqdm(range(0, len(train_X), batch_size)):
            batch_X = train_X[i:i + batch_size].view(-1, 1, self.img_size, self.img_size)
            batch_y = train_y[i:i + batch_size]

            batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)

            self.zero_grad()
            outputs = self(batch_X)
            loss = self.loss_function(outputs, batch_y)
            loss.backward()
            self.optimizer.step()

            matches = [torch.argmax(i) == torch.argmax(j) for i, j in zip(outputs, batch_y)]
            accuracy = matches.count(True)/len(matches)

            logfile.write(f"{int(time.time())},{epoch},in_sample,{round(float(accuracy),2)},{round(float(loss),4)}\n")
    
    # Test the model.
    # train_X is the input images
    # train_y is the input image classification in one-hot format: [1, 0] for cat, [0, 1] for dog
    # This data should be "out of sample" (ie not the same images used in training)
    def test(self, test_X, test_y):
        correct = 0
        total = 0
        with torch.no_grad():
            for i in range(len(test_X)):
                real_class = torch.argmax(test_y[i]).to(self.device)
                net_out = self(test_X[i].view(-1, 1, self.img_size, self.img_size).to(self.device))[0]

                predicted_class = torch.argmax(net_out)
                if predicted_class == real_class:
                    correct += 1
                total += 1
        print("Accuracy:", round(correct/total,3))