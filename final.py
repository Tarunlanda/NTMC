import random
from qiskit import QuantumCircuit, BasicAer, execute, ClassicalRegister
from qiskit.circuit.instructionset import InstructionSet

def bitwise_magnitude_comparison(a, b):
    # Make sure both a and b nhave the same length
    if len(a) != len(b):
        if(len(a)>len(b)):
          return "Alice > Bob"
        else:
          return "Alice < Bob"
    # Perform XOR and minimum operations for each bit position
    for i in range(len(a)):
        a_xor = int(a[i]) ^ 1
        b_xor = int(b[i]) ^ 1
        g = int(a[i]) & b_xor
        l = int(b[i]) & a_xor

        # Check the results
        if g == 1 and l != 1:
            return "Alice > Bob"
        elif l == 1 and g != 1:
            return "Alice < Bob"

    # If no inequality is found, return "a = b"
    return "Alice = Bob"

def generate_random_binary(n):
    binary_number = ''.join([str(random.randint(0, 1)) for _ in range(n)])
    return binary_number

def generate_random_bell_circuits(N):
    bell_circuits = []
    for _ in range(N):
        qc = QuantumCircuit(2,2)
        qc.h(0)
        qc.x(1)
        # Apply a CNOT gate with the first qubit as control and the second qubit as target
        if random.choice([True, False]):
            qc.cx(0, 1)  # Apply a CNOT gate
        else:
            qc.z(0) 
            qc.z(1)      
            qc.cx(0, 1)  
            # print('2',qc.draw())
        bell_circuits.append(qc)
    return bell_circuits

def divide_bell_circuits(bell_circuits):
    midpoint = len(bell_circuits) // 2
    sequence1 = bell_circuits[:midpoint]
    sequence2 = bell_circuits[midpoint:]
    # sequence1 = generate_random_bell_circuits(midpoint)
    # sequence2 = generate_random_bell_circuits(midpoint)
    return sequence1, sequence2

def convert_to_bits(circuits):
    measured_circuits = ""
    for qc in circuits:
        chosen_outcome = measure_circuit(qc)
        measured_circuits = measured_circuits + chosen_outcome
    return measured_circuits


def measure_circuit(qc):
    simulator = BasicAer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    # print(qc.draw())
    # print(list(counts.keys()))
    return list(counts.keys())[0]

def generate_random_decoy_states_circuits(N):
    circuits = []
    for _ in range(N):
        qc = QuantumCircuit(1)
        # Apply random gates
        state = random.choice(['0', '1', '+', '-'])
        if state == '0':
            pass  # No gate needed for state |0⟩
        elif state == '1':
            qc.x(0)  # Apply X gate for state |1⟩
        elif state == '+':
            qc.h(0)  # Apply H gate for state |+⟩
        else:
            qc.x(0)  # Apply X gate for state |-⟩
            qc.h(0)
        qc.measure_all()
        if(state == '0' or state == '1'):
          circuits.append((qc,'Z'))
        else:
          circuits.append((qc,'X'))
    return circuits
import random

def random_insert_decoy(decoy, bell_states):
    selected_positions = random.sample(range(len(bell_states)), len(decoy))
    decoy_positions = list(zip(decoy, selected_positions))
    decoy_positions.sort(key=lambda x: x[1])
    for (decoy_state, basis), position in decoy_positions:
        bell_states.insert(position, decoy_state)
    return bell_states, decoy_positions


def eaves_change(bell_states,insert_positions,name):
  for (decoy, basis), index in insert_positions:
    print(f"Do you want to change the Bell state at index {index} for {name}?")
    choice = input("Enter 'yes' to change, 'no' to keep: ").lower()
    if choice == 'yes':
      qc = (bell_states[index])
      bell_states[index] = qc.x(0)
    elif choice == 'no':
      print("No changes")
      break
  return bell_states

# def error_check(bell_states,insert_positions):
#   total = len(insert_positions)
#   matched = 0
#   for i in (total-1,-1):
#     calculated = bell_states[insert_positions[0][1]]
#     qc = insert_positions[0][0][0]
    # if insert_positions[0][0][1] == 'X':
    #   qc.h(0)
    #   calculated.h(0)
    # qc.measure(0,0)
    # calculated.measure(0,0)
    # simulator = BasicAer.get_backend('qasm_simulator')
    # job_true = execute(qc, simulator, shots=1)
    # result_true = job_true.result()
    # counts_true = result_true.get_counts(qc)
    # measurement_result_true = int(list(counts_true.keys())[0])
    # job_calculated = execute(calculated, simulator, shots=1)
    # result_calculated = job_calculated.result()
    # counts_calculated = result_calculated.get_counts(calculated)
    # measurement_result_calculated = int(list(counts_calculated.keys())[0])
    # if measurement_result_calculated == measurement_result_true:
    #   matched = matched +1
    # else:
    #   print(qc.draw())
    # print(qc.draw())
    # print(calculated.draw())
  #   if qc == calculated:
  #     matched = matched +1
  # return (1-(matched/total))

def error_check(SA, SA_1, DA_decoy_positions):
    total = len(DA_decoy_positions)
    unmatched = 0
    for qc2 in SA_1:
      if (isinstance(qc2, InstructionSet)):
          unmatched += 1
    return unmatched / total

def remove_decoy(bell_states,insert_positions):
  total = len(insert_positions)
  for i in (total-1,-1):
    del bell_states[insert_positions[0][1]]
  return bell_states

def calculate_encoded(quantity,key,TPV):
  final = ""
  for i in range(0,len(TPV)):
    final = final + str(int(quantity[i])+int(key[i])+int(TPV[i]))
  return final

def calculate_encoded_2(quantity,key):
  final = ""
  for i in range(0,len(quantity)):
    final = final + str(int(quantity[i])+int(key[i]))
  return final


# size = random.randint(4, 10)
size = 4
Alice = generate_random_binary(size)
bob = generate_random_binary(size)
TP_generated_bell_states = generate_random_bell_circuits(size)
BA,BB = divide_bell_circuits(TP_generated_bell_states)
maxi = (size)//2
decoy_size = random.randint(1,maxi)

DA = generate_random_decoy_states_circuits(decoy_size)
SA,insert_A = random_insert_decoy(DA,BA)
SA_1 = eaves_change(SA,insert_A,"Alice")
errorA = error_check(SA_1,SA,insert_A)
# print(insert_A)

DB = generate_random_decoy_states_circuits(decoy_size)
SB,insert_B = random_insert_decoy(DB,BB)
SB_1 = eaves_change(SB,insert_B,"Bob")
errorB = error_check(SB_1,SB,insert_B)
# print(errorA)
# print(errorB)
print("Error A = ",errorA)
print("Error B = ",errorB)

if errorA > 0.2 or errorB >0.2:
  print("Termination of Protocol")
else:
  BA_cal = remove_decoy(SA_1,insert_A)
  BB_cal = remove_decoy(SB_1,insert_B)
  BA_bits = convert_to_bits(BA_cal)
  BB_bits = convert_to_bits(BB_cal)
  KA = generate_random_binary(size)
  KB = generate_random_binary(size)
  # Alice = input(f"Alice quantity of size {size} bits in binary format")
  # Bob = input(f"Bob quantity of size {size} bits in binary format")
  Alice = generate_random_binary(size)
  Bob = generate_random_binary(size)
  # Alice = "1111"
  # Bob = "0001"
  print(f"Alice magnitude = {Alice}")
  print(f"Bob Magnitude = {Bob}")
  ra_bits = calculate_encoded(Alice,KA,BA_bits)
  # print(Alice,KA,BA_bits)
  rb_bits = calculate_encoded(Bob,KB,BB_bits)
  # print(ra_bits)
  ma_bits = calculate_encoded_2(ra_bits,KA)
  mb_bits = calculate_encoded_2(rb_bits,KB)
  answer = bitwise_magnitude_comparison(ma_bits,mb_bits)
  print(f"final comparision of the magnitudes {answer}")
