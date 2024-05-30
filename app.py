import streamlit as st
from qiskit import IBMQ, Aer, execute, QuantumCircuit
from qiskit.providers.ibmq import least_busy

# Get the IBM Qiskit API token from Streamlit secrets
API_TOKEN = st.secrets["IBM_QUANTUM_API_TOKEN"]

# Load your IBM Qiskit account
IBMQ.save_account(API_TOKEN, overwrite=True)
provider = IBMQ.load_account()

# Get the least busy backend
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 5 and
                                                  not x.configuration().simulator and x.status().operational==True))

# Function to run a quantum circuit
def run_quantum_circuit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0,1], [0,1])
    
    job = execute(qc, backend, shots=1024)
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
