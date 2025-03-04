import pandas as pd
import numpy as np

# Load data
data = pd.read_excel("room.xlsx", sheet_name="room_t")  # Replace with your actual file path

# Preprocess the data
features = data[['humidity', 'co2', 'desiredT', 'upperbound', 'lowerbound', 'occupancy']].values
targets = data['temperature'].values

# Normalize features
features_norm = (features - np.mean(features, axis=0)) / np.std(features, axis=0)
targets_norm = (targets - np.mean(targets)) / np.std(targets)

# Neural network parameters
input_size = features_norm.shape[1]
hidden_size = 10
output_size = 1
learning_rate = 0.01
epochs = 1000

# Initialize weights randomly
np.random.seed(42)
W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

# Activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Training loop
for epoch in range(epochs):
    # Forward pass
    z1 = np.dot(features_norm, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    output = z2  # Linear activation for output layer

    # Compute loss (Mean Squared Error)
    loss = np.mean((output - targets_norm.reshape(-1, 1))**2)

    # Backpropagation
    output_error = output - targets_norm.reshape(-1, 1)
    dW2 = np.dot(a1.T, output_error) / len(features_norm)
    db2 = np.sum(output_error, axis=0, keepdims=True) / len(features_norm)
    
    hidden_error = np.dot(output_error, W2.T) * sigmoid_derivative(a1)
    dW1 = np.dot(features_norm.T, hidden_error) / len(features_norm)
    db1 = np.sum(hidden_error, axis=0) / len(features_norm)

    # Update weights and biases
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2
    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1

    # Print loss every 100 epochs
    if epoch % 100 == 0:
        print(f'Epoch {epoch}, Loss: {loss}')

# Denormalize the prediction
predictions = output * np.std(targets) + np.mean(targets)

print(predictions)
