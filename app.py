import streamlit as st
import pennylane as qml
from pennylane import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from qiskit import IBMQ

# Initialize IBMQ account
IBMQ.load_account()

# Set up the device
dev = qml.device('qiskit.aer', wires=2)

# Define the quantum node
@qml.qnode(dev)
def circuit(params, x):
    qml.AngleEmbedding(x, wires=[0, 1])
    qml.StronglyEntanglingLayers(params, wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

# Define the cost function
def cost(params, X, Y):
    predictions = [circuit(params, x) for x in X]
    return np.mean((predictions - Y)**2)

# Load and preprocess data
X, Y = make_moons(n_samples=100, noise=0.1, random_state=42)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize parameters
params = np.random.randn(3, 2, 3)

# Optimize the parameters
opt = qml.GradientDescentOptimizer(stepsize=0.1)
epochs = 100
for epoch in range(epochs):
    params = opt.step(lambda v: cost(v, X_train, Y_train), params)

# Evaluate the model
predictions = [circuit(params, x) for x in X_test]
accuracy = np.mean((np.sign(predictions) == Y_test))
st.write(f"Accuracy: {accuracy * 100:.2f}%")

# Streamlit interface
st.title("Quantum Machine Learning with Qiskit and PennyLane")
st.header("Model Accuracy")
st.write(f"Accuracy on test data: {accuracy * 100:.2f}%")
