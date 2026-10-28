"""
QFT vs Classical FFT
Comparative Study of Quantum Fourier Transform and Classical Fast Fourier Transform

Run:
    python main.py

Outputs are saved in the results/ directory.
"""

from pathlib import Path
import time
import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, StatePreparation
from qiskit.quantum_info import Statevector


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def run_experiment(signal, experiment_name):
    """Compare QFT amplitudes with the equivalent normalized classical FFT result."""
    signal = np.asarray(signal, dtype=complex)
    n = len(signal)

    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError("Signal length must be a positive power of 2.")

    norm = np.linalg.norm(signal)
    if np.isclose(norm, 0):
        raise ValueError("Input signal must not be all zeros.")

    num_qubits = int(np.log2(n))
    normalized_signal = signal / norm

    # Classical forward FFT (negative exponent convention).
    t0 = time.perf_counter()
    classical_fft = np.fft.fft(signal)
    classical_seconds = time.perf_counter() - t0

    # QFTGate uses the positive-exponent convention. NumPy's ifft
    # uses the corresponding positive exponent and a 1/N factor.
    expected_qft = np.sqrt(n) * np.fft.ifft(signal) / norm

    # Prepare the input amplitudes, then apply QFT.
    qc = QuantumCircuit(num_qubits)
    qc.append(StatePreparation(normalized_signal), range(num_qubits))
    qc.append(QFTGate(num_qubits), range(num_qubits))

    t0 = time.perf_counter()
    quantum_state = Statevector.from_instruction(qc)
    quantum_seconds = time.perf_counter() - t0
    quantum_output = quantum_state.data

    max_error = float(np.max(np.abs(quantum_output - expected_qft)))
    matches = bool(np.allclose(quantum_output, expected_qft, atol=1e-8))

    # Save circuit diagram (text is reliable; matplotlib rendering is optional).
    circuit_text_path = RESULTS / f"{experiment_name}_circuit.txt"
    circuit_text_path.write_text(str(qc.draw(output="text")), encoding="utf-8")

    try:
        fig = qc.draw(output="mpl")
        fig.savefig(RESULTS / f"{experiment_name}_circuit.png", dpi=180, bbox_inches="tight")
        plt.close(fig)
    except Exception as exc:
        print(f"Note: circuit PNG could not be created ({exc}). Text diagram was saved.")

    indices = np.arange(n)

    # Magnitude comparison.
    plt.figure(figsize=(8, 4.8))
    plt.plot(indices, np.abs(quantum_output), "o-", label="Quantum QFT amplitudes")
    plt.plot(indices, np.abs(expected_qft), "s--", label="Normalized classical equivalent")
    plt.xlabel("Output index")
    plt.ylabel("Magnitude")
    plt.title(f"QFT vs Classical FFT — {experiment_name}")
    plt.xticks(indices)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / f"{experiment_name}_magnitude.png", dpi=180)
    plt.close()

    # Real and imaginary components.
    plt.figure(figsize=(8, 4.8))
    plt.plot(indices, quantum_output.real, "o-", label="QFT real")
    plt.plot(indices, expected_qft.real, "s--", label="FFT-equivalent real")
    plt.plot(indices, quantum_output.imag, "o-", label="QFT imaginary")
    plt.plot(indices, expected_qft.imag, "s--", label="FFT-equivalent imaginary")
    plt.xlabel("Output index")
    plt.ylabel("Amplitude")
    plt.title(f"Complex amplitude comparison — {experiment_name}")
    plt.xticks(indices)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / f"{experiment_name}_complex.png", dpi=180)
    plt.close()

    # Save a readable numerical report.
    report_path = RESULTS / f"{experiment_name}_results.txt"
    report_path.write_text(
        f"Experiment: {experiment_name}\n"
        f"Input signal: {np.array2string(signal)}\n"
        f"Number of input values: {n}\n"
        f"Number of qubits: {num_qubits}\n\n"
        f"Classical FFT: {np.array2string(classical_fft, precision=6)}\n"
        f"QFT amplitudes: {np.array2string(quantum_output, precision=6)}\n"
        f"Expected QFT amplitudes: {np.array2string(expected_qft, precision=6)}\n\n"
        f"Maximum absolute error: {max_error:.12g}\n"
        f"Validation: {'PASS' if matches else 'CHECK'}\n"
        f"Classical FFT wall-clock time (one run): {classical_seconds:.8f} seconds\n"
        f"Statevector simulation wall-clock time (one run): {quantum_seconds:.8f} seconds\n\n"
        "Timing note: these are single local runs and are not a fair quantum-vs-classical speed benchmark.\n"
        "The statevector simulator runs on a classical computer.\n",
        encoding="utf-8",
    )

    print(f"\n=== {experiment_name} ===")
    print("Input:", signal)
    print("Qubits:", num_qubits)
    print("Classical FFT:", np.round(classical_fft, 5))
    print("QFT amplitudes:", np.round(quantum_output, 5))
    print("Expected QFT amplitudes:", np.round(expected_qft, 5))
    print(f"Maximum absolute error: {max_error:.3e}")
    print("Validation:", "PASS" if matches else "CHECK")
    print(f"Saved outputs in: {RESULTS}")

    return {
        "experiment": experiment_name,
        "n": n,
        "qubits": num_qubits,
        "max_error": max_error,
        "validation": "PASS" if matches else "CHECK",
        "classical_seconds": classical_seconds,
        "statevector_seconds": quantum_seconds,
    }


def main():
    experiments = [
        ("experiment_1", [1, 0]),
        ("experiment_2", [1, 0, 1, 0]),
        ("experiment_3", [1, 2, 0, 1, 0, 1, 0, 0]),
    ]

    summaries = [run_experiment(signal, name) for name, signal in experiments]

    # Summary table as CSV for the report.
    csv_path = RESULTS / "summary.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        f.write("experiment,input_size,qubits,max_absolute_error,validation,classical_seconds,statevector_seconds\n")
        for row in summaries:
            f.write(
                f"{row['experiment']},{row['n']},{row['qubits']},"
                f"{row['max_error']:.12g},{row['validation']},"
                f"{row['classical_seconds']:.8f},{row['statevector_seconds']:.8f}\n"
            )

    print("\nAll experiments finished.")
    print(f"Summary CSV: {csv_path}")
    print("Review the images and result text files inside the results/ folder.")


if __name__ == "__main__":
    main()
