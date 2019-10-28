import math
import random
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.tools.visualization import circuit_drawer
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.visualization import plot_state_city, plot_bloch_multivector, plot_state_paulivec, plot_state_hinton, plot_state_qsphere

import time
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy

qr = QuantumRegister(3, 'q')
cr = ClassicalRegister(1, 'c')
qc = QuantumCircuit(qr, cr)

# ====== PART 1 ====== #
# Generarte Alice's input state |Psi> = \alpha|0> + \beta|1>
# here: \psi> = 1/sqrt{2}(|0> + |1>)
qc.h(qr[0])

# ====== PART 2 ====== #
# Generate Bell-States to be shared between Alice and Bob
qc.h(qr[1])
qc.cx(qr[1], qr[2])


# ====== PART 3 ====== #
# Bell Measurement on both of Alice's qubits
qc.cx(qr[0], qr[1])
qc.h(qr[0])

# This will create a superposition of four terms:
# |ψ⟩ =  􏰇1/2 *[ |00⟩(α|0⟩ + β(|1⟩) + |01⟩(α|1⟩ + β(|0⟩) + |10⟩(α|0⟩ - β(|1⟩) + |11⟩(α|1⟩ - β(|0⟩)]􏰈

# first two qubits of Alice:
# If |00⟩ -> Apply Id 	to Bob's qubit
# If |01⟩ -> Apply X 	to Bob's qubit
# If |10⟩ -> Apply Z 	to Bob's qubit
# If |11⟩ -> Apply X.Z 	to Bob's qubit

# ====== PART 3 ====== #
# Apply X-Gate to Bob's Qubit if Alice's 2nd Qubit is 1 -> CNOT to Bob's qubit
qc.cx(qr[1], qr[2]) 

# Apply Z-Gate to Bob's Qubit if Alice's 1st Qubit is 1 -> Controlled Z Gate = H-CNOT-H ot Bob's qubit
qc.cz(qr[0], qr[2])
# qc.h(qr[2])
# qc.cx(qr[0], qr[2])
# qc.h(qr[2])

qc.measure(qr[2], cr[0])

# ========== DRAW CIRCUIT =============
# requires latex to be installed
qc.draw(output='latex',interactive=True)


# ========== SIMULATION ==========
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim, shots=1000)
result_sim = job_sim.result()
counts = result_sim.get_counts()
print(counts)

# ========== REAL EXECTUTION ==========
IBMQ.load_accounts()
print("\n(IBMQ Backends)")
print(IBMQ.backends())

# auto-select least beasy device:
device = least_busy(IBMQ.backends(simulator=False))
print("Running on current least busy device: ", device)
# manually fix backend device (in case of errors):
# device = IBMQ.get_backend('ibmqx4')
# device = IBMQ.get_backend('ibmqx2')
# device = IBMQ.get_backend('ibmq_16_melbourne')
# print(device.status())

job_exp = execute(qc, backend=device, shots=1000, max_credits=10)

lapse = 0
interval = 10
print('Job ID: ',job_exp.job_id())
print('Backend: ',device.name())
while job_exp.status().name != 'DONE':
    print('Status @ {} seconds'.format(interval * lapse),': ',job_exp.status(),' Queue Position:',job_exp.queue_position())
    time.sleep(interval)
    lapse += 1
print(job_exp.status())
result_exp = job_exp.result()

print("experiment: ", result_exp)
print(result_exp.get_counts())
# plot_histogram(result_exp.get_counts(qc)).savefig('histo.png')



