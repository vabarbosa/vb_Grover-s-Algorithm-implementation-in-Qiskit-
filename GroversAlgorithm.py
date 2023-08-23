from qiskit import QuantumCircuit, transpile, assemble, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.providers.ibmq import least_busy

# Define the number of qubits and the target element to search for
n = 3  # Number of qubits (2^n states)
target = '101'  # Binary representation of the target element

# Create the oracle
oracle = QuantumCircuit(n+1)
for qubit in range(n):
    oracle.cx(qubit, n)  # Apply controlled-X gate from qubit to target qubit if qubit's value is 1
oracle.draw()

# Create the Grover diffusion operator
grover_diffusion = QuantumCircuit(n)
for qubit in range(n):
    grover_diffusion.h(qubit)
for qubit in range(n):
    grover_diffusion.x(qubit)
grover_diffusion.h(n-1)
grover_diffusion.mct(list(range(n-1)), n-1)  # Multi-controlled Toffoli gate
grover_diffusion.h(n-1)
for qubit in range(n):
    grover_diffusion.x(qubit)
for qubit in range(n):
    grover_diffusion.h(qubit)
grover_diffusion.draw()

# Create the full Grover circuit
grover_circuit = QuantumCircuit(n+1, n)
grover_circuit.h(range(n))
grover_circuit.x(n)
grover_circuit.h(n)
grover_circuit.append(oracle, range(n+1))
grover_circuit.append(grover_diffusion, range(n))
grover_circuit.measure(range(n), range(n))
grover_circuit.draw()

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
job = execute(grover_circuit, simulator, shots=1024)
result = job.result()
counts = result.get_counts()
plot_histogram(counts)

# Find the most probable solution
most_probable = max(counts, key=counts.get)
print("Most probable solution:", most_probable)
