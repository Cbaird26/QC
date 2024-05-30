import streamlit as st
from qiskit import Aer, execute, QuantumCircuit

# Function to run a quantum circuit
def run_quantum_circuit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0,1], [0,1])
    
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    return counts

# Function to generate chatbot response using quantum result
def get_bot_response(user_input):
    quantum_result = run_quantum_circuit()
    # Use quantum_result to influence the chatbot response
    response = f"The quantum result is: {quantum_result}. Your input was: {user_input}"
    return response

# Streamlit app interface
st.title("Quantum Chatbot")
user_input = st.text_input("You: ", "Type your message here...")

if st.button("Send"):
    response = get_bot_response(user_input)
    st.text_area("Bot: ", value=response, height=200, max_chars=None)
