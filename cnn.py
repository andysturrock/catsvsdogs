import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class CNN(nn.Module):
    def __init__(self, device):
        super().__init__()
        self.device = device

        self.conv1 = nn.Conv2d(1, 32, 5)
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.conv3 = nn.Conv2d(64, 128, 5)

        x = torch.randn(50,50).view(-1,1,50,50)
        self._to_linear = None
        self.convs(x)

        self.fc1 = nn.Linear(self._to_linear, 512)
        self.fc2 = nn.Linear(512, 2)

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.loss_function = nn.MSELoss()

    def convs(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2,2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2,2))

        if self._to_linear is None:
            self._to_linear = x[0].shape[0]*x[0].shape[1]*x[0].shape[2]
        return x

    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, self._to_linear)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

    def train(self, epochs, batch_size, train_X, train_y):
        for epoch in range(epochs):
            for i in range(0, len(train_X), batch_size):
                batch_X = train_X[i:i + batch_size].view(-1, 1, 50, 50)
                batch_y = train_y[i:i + batch_size]

                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)

                self.zero_grad()
                outputs = self(batch_X)
                loss = self.loss_function(outputs, batch_y)
                loss.backward()
                self.optimizer.step()

                matches = [torch.argmax(i) == torch.argmax(j) for i, j in zip(outputs, y)]
                acc = matches.count(True)/len(matches)
                loss = self.loss_function(outputs, y)

                print(f"Acc: {round(float(acc),2)}  Loss: {round(float(loss),4)}")
    
    def test(self, test_X, test_y):
        correct = 0
        total = 0
        with torch.no_grad():
            for i in range(len(test_X)):
                real_class = torch.argmax(test_y[i]).to(self.device)
                net_out = self(test_X[i].view(-1, 1, 50, 50).to(self.device))[0]

                predicted_class = torch.argmax(net_out)
                if predicted_class == real_class:
                    correct += 1
                total += 1
        print("Accuracy:", round(correct/total,3))