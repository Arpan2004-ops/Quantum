# Comparative Study of Quantum Fourier Transform and Classical FFT

## 1. Abstract
Write a short summary of the objective, implementation, experiments, and main result.

## 2. Problem Statement
Explain why the project compares a quantum transform with a classical transform.

## 3. Objectives
- Implement QFT using Qiskit.
- Implement classical FFT using NumPy.
- Compare outputs for small power-of-two input sizes.
- Validate the numerical relationship and visualise the results.

## 4. Theory
### 4.1 Discrete Fourier Transform
Add the DFT formula and explain the frequency coefficients.

### 4.2 Classical FFT
Explain that FFT is an efficient algorithm for calculating the DFT.

### 4.3 Quantum Fourier Transform
Add the QFT formula and explain amplitudes and phase factors.

## 5. Tools and Requirements
Python, Qiskit, NumPy, Matplotlib, and the local statevector simulator.

## 6. Methodology
Describe input normalisation, quantum state preparation, QFT application, classical FFT, convention adjustment, and numerical validation.

## 7. Experiments
Record the input, input length, qubit count, maximum absolute error, validation result, and graph filenames for all three experiments.

## 8. Results and Discussion
Insert the circuit and generated plots from `results/`. Explain whether the numerical outputs match and what the plots show.

## 9. Complexity and Limitations
Discuss the usual asymptotic costs carefully. The standard classical FFT takes O(N log N) time. A standard QFT circuit uses O(n^2) elementary gates for n = log2(N) qubits, with more efficient approximate variants possible. Statevector simulation has classical memory/time costs that grow exponentially with the number of qubits. This small simulator experiment does not establish quantum speedup.

## 10. Individual Contributions
- Member 1:
- Member 2:
- Member 3:

## 11. Conclusion
Summarise the implementation and the validation results actually obtained.

## 12. References
Add official Qiskit documentation, NumPy FFT documentation, and relevant course material.
