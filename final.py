from qiskit import QuantumCircuit, execute, BasicAer, QuantumRegister, ClassicalRegister
import numpy as np

# Function for the minimum operation
def minimum_operation(a, b):
    # Perform exclusive-OR operations with 1
    a_bar = a ^ 1
    b_bar = b ^ 1

    # Perform the minimum operation
    g = a_bar & b
    l = b_bar & a

    # Determine the relationship based on the result
    if g:
        return "A > B"
    elif l:
        return "A < B"
    else:
        return "A = B"

# Step 0: Key Generation
def generate_shared_key(N):
    # Generate random key sequence
    return ''.join(np.random.choice(['0', '1']) for _ in range(N))

# Step 1: Bell State Generation and Photon Insertion
def generate_bell_states(N):
    qr = QuantumRegister(2*N)
    qc = QuantumCircuit(qr)
    for qubit in range(N):
        qc.h(qubit)
        qc.cx(qubit, qubit+N)
    return qc

def insert_decoy_photons(qc, N):
    cr = ClassicalRegister(N)  # Create a classical register with N bits
    qc.add_register(cr)  # Add the classical register to the quantum circuit
    # Insert decoy photons
    for qubit in range(N):
        decoy = np.random.choice(['0', '1', '+', '-'])
        if decoy == '0':
            qc.measure(qubit, qubit)
        elif decoy == '1':
            qc.x(qubit)
            qc.measure(qubit, qubit)
        elif decoy == '+':
            qc.h(qubit)
            qc.measure(qubit, qubit)
        elif decoy == '-':
            qc.x(qubit)
            qc.h(qubit)
            qc.measure(qubit, qubit)
    return qc

# Step 3: Measurement and Exclusive-OR Operations
def measure_xor_operations(qc, shared_key, N):
    # Measure and perform XOR operations
    measured_bits = ''
    for qubit in range(N):
        if shared_key[qubit] == '0':
            qc.measure((0, qubit), (0, qubit))
        elif shared_key[qubit] == '1':
            qc.measure((0, qubit + N), (0, qubit))
        measured_bits += shared_key[qubit]
    return qc, measured_bits



# Check for eavesdropping
def check_eavesdropping(shared_key, measured_bits):
    errors = sum([shared_key[i] != measured_bits[i] for i in range(len(shared_key))])
    error_rate = errors / len(shared_key)
    return error_rate

# Step 4: Computation and Comparison
def compute_comparison_results(m0, m1, N):
    comparison_result = ''
    for j in range(N):
        if m0[j] == '0':
            comparison_result += m1[j]
            break
        elif m0[j] == '1':
            comparison_result += '1'
            break
    return comparison_result

# Step 5: Interpretation
def interpret_results(comparison_result, measured_bits):
    if comparison_result == '0':
        print("Alice is wealthier") if measured_bits[0] == '0' else print("Bob is wealthier")
    else:
        print("Bob is wealthier") if measured_bits[0] == '0' else print("Alice is wealthier")

if __name__ == "__main__":
    # Parameters
    N = 4  # Number of qubits

    # Get input from the user for A and B
    A = int(input("Enter the value of A (integer): "))
    B = int(input("Enter the value of B (integer): "))

    # Step 0: Key Generation
    KA = generate_shared_key(N)
    KB = generate_shared_key(N)

    # Step 1: Bell State Generation and Photon Insertion
    qc = generate_bell_states(N)
    qc = insert_decoy_photons(qc, N)

    # Step 3: Measurement and Exclusive-OR Operations
    qc, measured_bits = measure_xor_operations(qc, KA, N)

    # Execute the circuit
    backend = BasicAer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1)
    counts = job.result().get_counts()
    print("Measured bits:", measured_bits)
    print("Measurement outcome:", list(counts.keys())[0])

    # Check for eavesdropping
    error_rate = check_eavesdropping(KA, measured_bits)
    print("error rate = ",error_rate)
    if error_rate > 0.1:  # Arbitrary threshold for error rate
        print("Eavesdropping detected!")
    else:
        print("No eavesdropping detected.")

    # Step 5: Interpretation
    comparison_result = compute_comparison_results(KA, KB, N)
    print("comparision = ",comparison_result)
    interpret_results(comparison_result, measured_bits)

    # Perform minimum operation on A and B
    result = minimum_operation(A, B)
    print("Result of minimum operation:", result)