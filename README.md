# QFT vs Classical FFT

**Project title:** Comparative Study of Quantum Fourier Transform and Classical Fast Fourier Transform

## Objective

Implement the Quantum Fourier Transform (QFT) using Qiskit, compare its output with a classical FFT using NumPy, and validate that the outputs match after accounting for normalisation and exponent-sign conventions.

## Team of three

- **Member 1 — Quantum implementation:** explain qubits, state preparation, QFT circuit, and circuit diagram.
- **Member 2 — Classical FFT:** explain DFT/FFT, NumPy implementation, complex values, and normalisation.
- **Member 3 — Experiments and analysis:** run experiments, interpret graphs and errors, assemble the report and presentation.

All members should understand the whole program and be able to answer questions about it.

## Requirements

- Python 3.10 or newer recommended
- pip
- Qiskit
- NumPy
- Matplotlib

## Setup on Windows PowerShell

Open PowerShell in this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Run terminal experiments:
python main.py

# Launch interactive Streamlit dashboard:
python -m streamlit run dashboard.py
```

Or double-click `run_streamlit.bat` directly in File Explorer.

If PowerShell blocks activation, you can run the environment directly:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\streamlit.exe run dashboard.py
```

## Interactive Streamlit Dashboard (`dashboard.py`)

The dashboard features:
- **A. Input Signal Panel (Sidebar):** Select predefined signals ($N=2, 4, 8$) or enter custom inputs.
- **B. Quantum Circuit Panel:** QFT circuit diagram with gate legend ($H$, $R_2$, $X$, Measurement).
- **C. Magnitude Comparison:** Line plot comparing Quantum QFT with normalized classical FFT.
- **D. Real and Imaginary Components:** Complex amplitude decomposition line chart.
- **E. Validation and Results:** Machine precision error, signal length, qubit count, and normalization factor.
- **F. Numerical Results & CSV Export:** Full index table with download button.
- **Key Takeaways & Team Info:** Mathematical summary and team presentation pointers.

## What the program does

1. Uses three input signals with lengths 2, 4, and 8.
2. Normalises each signal so it can be encoded as a quantum state.
3. Uses Qiskit's `StatePreparation` and `QFTGate` to simulate QFT.
4. Uses NumPy's FFT and inverse FFT convention to form the corresponding QFT amplitudes.
5. Validates the results using maximum absolute error and `np.allclose`.
6. Saves circuit diagrams, magnitude plots, complex-amplitude plots, text reports, and a CSV summary in `results/`.

## Expected result

Each experiment should print `Validation: PASS`, with numerical error close to floating-point precision.

## Important interpretation

- QFT uses a positive phase exponent; NumPy's forward FFT uses a negative exponent.
- QFT amplitudes are normalised. The program accounts for this when comparing the classical result.
- The code uses an ideal statevector simulator, not a physical quantum computer.
- Execution times are included only as observations from one local run. They are **not** a fair benchmark proving QFT is faster than FFT.
- This project demonstrates mathematical equivalence for small examples; it does not demonstrate quantum advantage.

## Output files

All outputs are saved to `results/`:

- `*_circuit.txt` — text circuit diagram
- `*_circuit.png` — circuit image, if the installed plotting dependencies support it
- `*_magnitude.png` — magnitude comparison
- `*_complex.png` — real/imaginary comparison
- `*_results.txt` — numerical results and validation
- `summary.csv` — experiment summary

## Suggested report structure

1. Abstract
2. Introduction and problem statement
3. Objectives
4. Background: DFT, FFT, QFT, quantum states
5. Methodology and circuit design
6. Implementation
7. Experiments and results
8. Discussion and limitations
9. Individual contributions
10. Conclusion
11. References

## Suggested viva topics

- What is a qubit?
- What are superposition and measurement?
- What does QFT do to amplitudes?
- How does QFT relate to the discrete Fourier transform?
- Why are the input amplitudes normalised?
- Why do FFT and QFT outputs need convention adjustment?
- Why does a statevector simulator not prove quantum speedup?
