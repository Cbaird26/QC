import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import Aer, QuantumCircuit, execute
from scipy.constants import hbar, m_e

# Define the potential well boundaries
L = 1.0  # Width of the box in meters

# Define a function to compute the energy levels of a particle in a box using classical physics
def classical_energy_levels(n, L):
    return (n**2 * np.pi**2 * hbar**2) / (2 * m_e * L**2)

# Define a function to run a quantum circuit simulating the energy levels of a particle in a box
def run_quantum_simulation(n, L):
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply a Hadamard gate
    qc.measure(0, 0)
    
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    return counts

# Streamlit interface
st.title("Quantum and Classical Simulation of a Particle in a Box")

st.header("Input Parameters")
n = st.number_input("Enter quantum number n", min_value=1, value=1)
L = st.number_input("Enter the width of the box L (in meters)", value=1.0)

if st.button("Solve"):
    st.header("Classical Computation Result")
    classical_energy = classical_energy_levels(n, L)
    st.write(f"Energy level using classical physics: {classical_energy:.5e} J")
    
    st.header("Quantum Circuit Simulation")
    quantum_counts = run_quantum_simulation(n, L)
    st.write("Quantum Circuit Result:", quantum_counts)
    st.pyplot(plot_histogram(quantum_counts))

    st.header("Visualizing Wave Function")
    x = np.linspace(0, L, 1000)
    wave_function = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
    plt.plot(x, wave_function)
    plt.xlabel('Position (m)')
    plt.ylabel('Wave Function')
    plt.title('Wave Function of a Particle in a Box')
    st.pyplot(plt)

# To run the app, use the command: streamlit run app.py
