import matplotlib.pyplot as plt
from Tensor import *

from nn import Linear, ReLU, LogSoftmax, Sigmoid

from Loss import NLLLoss

from optim import SGD

from GetMNIST import fetch_mnist


class Network():

    def __init__(self):
        self.fc1 = Linear(784, 128)
        self.fc2 = Linear(128, 10)
        self.logsoftmax = LogSoftmax()
        self.relu = ReLU()
        self.sigmoid = Sigmoid()

    def forward(self, input):
        x = self.sigmoid(self.fc1(input))
        x = self.fc2(x)
        return self.logsoftmax(x, 1)

    def parameters(self):
        return [self.fc1.weights, self.fc2.weights, self.fc1.bias, self.fc2.bias]


model = Network()
optimizer = SGD(model.parameters(), lr=0.1)
criterion = NLLLoss()

# Batching code
X_train, Y_train, X_test, Y_test = fetch_mnist()

epochs = 1
losses = []

for i in range(0, epochs):
    samp = np.random.randint(0, X_train.shape[0], size=(64))

    x = Tensor(X_train[samp].reshape((-1, 28*28)).astype(np.float32))
    Y = Y_train[samp]
    y = np.zeros((len(samp), 10), np.float32)
    # correct loss for NLL, torch NLL loss returns one per row
    y[range(y.shape[0]), Y] = 1
    y = Tensor(y)

    optimizer.zero_grad()

    out = model.forward(x)
    # print(out)
    loss = criterion(out, y)
    loss.backward()
    losses.append(loss.value)
    optimizer.step()
    # print(loss)

# plt.plot(range(0, epochs), losses)
# plt.show()
