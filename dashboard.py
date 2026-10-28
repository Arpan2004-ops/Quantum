"""
QFT vs Classical FFT - Interactive Streamlit Dashboard
Comparative Study of Quantum Fourier Transform and Classical Fast Fourier Transform
"""

import io
import re
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, StatePreparation
from qiskit.quantum_info import Statevector

# -----------------------------------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="QFT vs Classical FFT",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Custom Cyber-Dark CSS Styling matching exact layout of Image 1
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@500;600;700;800&display=swap');

    /* Global page styling */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #060b15 !important;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0a1120 !important;
        border-right: 1px solid #172540 !important;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif;
    }

    /* Cards */
    .dashboard-card {
        background: #0d1527;
        border: 1px solid #1a2744;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }

    .card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }

    /* Header Styling */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        padding: 14px 20px;
        background: #09101f;
        border: 1px solid #172540;
        border-radius: 12px;
        margin-bottom: 20px;
        gap: 16px;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .header-logo {
        font-size: 2.2rem;
        color: #38bdf8;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .header-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.45rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 0.82rem;
        color: #94a3b8;
    }

    .header-badges {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.78rem;
        color: #94a3b8;
    }

    .team-badge {
        background: #111e38;
        border: 1px solid #1e3358;
        border-radius: 8px;
        padding: 6px 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #e2e8f0;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Success Box */
    .success-card {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 8px;
        padding: 14px 16px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 16px;
    }

    .success-icon {
        background: #10b981;
        color: #060b15;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9rem;
        flex-shrink: 0;
    }

    .success-title {
        color: #10b981;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 2px;
    }

    .success-desc {
        color: #94a3b8;
        font-size: 0.78rem;
        line-height: 1.4;
    }

    /* Metrics List */
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 0;
        border-bottom: 1px solid #152238;
        font-size: 0.83rem;
    }

    .metric-row:last-child {
        border-bottom: none;
    }

    .metric-name {
        color: #94a3b8;
    }

    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        color: #f1f5f9;
    }

    /* Takeaways List */
    .takeaway-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 0.82rem;
        color: #cbd5e1;
        margin-bottom: 10px;
        line-height: 1.45;
    }

    .takeaway-icon {
        color: #10b981;
        font-size: 0.9rem;
        font-weight: bold;
        flex-shrink: 0;
        margin-top: 1px;
    }

    /* Circuit Legend Badges */
    .circuit-legend {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px solid #16243d;
        font-size: 0.75rem;
    }

    .legend-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
    }

    .tag-h {
        background: #0284c7;
        color: #ffffff;
    }

    .tag-r {
        background: #9333ea;
        color: #ffffff;
    }

    .tag-x {
        background: #db2777;
        color: #ffffff;
    }

    .tag-m {
        background: #1e293b;
        border: 1px solid #334155;
        color: #cbd5e1;
    }

    /* Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0284c7, #2563eb) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3) !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #0369a1, #1d4ed8) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.45) !important;
    }

    /* Inputs */
    div[data-baseweb="input"] {
        background-color: #0d1527 !important;
        border-color: #1e293b !important;
        border-radius: 6px !important;
        color: #f8fafc !important;
    }

    /* Footer */
    .dashboard-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 4px 8px;
        margin-top: 24px;
        border-top: 1px solid #142036;
        font-size: 0.75rem;
        color: #64748b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# QFT Simulation & Mathematical Core
# -----------------------------------------------------------------------------
def analyze_signal(signal_input):
    """
    Validates input signal, simulates QFT via Qiskit, computes classical FFT,
    and returns metrics and dataframes.
    """
    signal = np.asarray(signal_input, dtype=complex)
    n = len(signal)

    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError(f"Signal length must be a power of 2 (2, 4, 8, ...). Given length: {n}")

    norm = np.linalg.norm(signal)
    if np.isclose(norm, 0):
        raise ValueError("Input signal cannot be all zeros.")

    num_qubits = int(np.log2(n))
    normalized_signal = signal / norm
    norm_factor = 1.0 / np.sqrt(n)

    # Classical forward FFT
    classical_fft = np.fft.fft(signal)

    # Expected QFT equivalent via NumPy's IFFT (accounting for convention and normalization)
    expected_qft = np.sqrt(n) * np.fft.ifft(signal) / norm

    # Quantum Simulation using Qiskit
    qc = QuantumCircuit(num_qubits)
    qc.append(StatePreparation(normalized_signal), range(num_qubits))
    qc.append(QFTGate(num_qubits), range(num_qubits))

    state = Statevector.from_instruction(qc)
    quantum_output = state.data

    # Error calculation
    diff = np.abs(quantum_output - expected_qft)
    max_error = float(np.max(diff))
    is_match = bool(np.allclose(quantum_output, expected_qft, atol=1e-8))

    # Helper to format numbers cleanly
    def fmt_num(val):
        if np.isclose(val.imag, 0, atol=1e-12):
            return f"{val.real:.4f}"
        sign = "+" if val.imag >= 0 else "-"
        return f"{val.real:.4f} {sign} {abs(val.imag):.4f}j"

    # Numerical results DataFrame with both Classical and Quantum values
    table_rows = []
    for i in range(n):
        basis_str = f"|{bin(i)[2:].zfill(num_qubits)}⟩"
        x_val = signal[i]
        in_amp = normalized_signal[i]
        c_raw = classical_fft[i]
        c_norm = expected_qft[i]
        q_val = quantum_output[i]
        d_val = diff[i]
        table_rows.append(
            {
                "Index": i,
                "Basis State": basis_str,
                "Classical Input x[k]": fmt_num(x_val),
                "Quantum State Prep": fmt_num(in_amp),
                "Classical FFT X[k] (Raw)": fmt_num(c_raw),
                "Classical FFT (Normalized)": fmt_num(c_norm),
                "Quantum QFT Amplitude": fmt_num(q_val),
                "Difference": f"{d_val:.4e}",
            }
        )
    df_results = pd.DataFrame(table_rows)

    return {
        "signal": signal,
        "normalized_signal": normalized_signal,
        "n": n,
        "num_qubits": num_qubits,
        "norm": norm,
        "norm_factor": norm_factor,
        "quantum_output": quantum_output,
        "expected_qft": expected_qft,
        "classical_fft": classical_fft,
        "max_error": max_error,
        "is_match": is_match,
        "df_results": df_results,
    }


# -----------------------------------------------------------------------------
# Matplotlib Dark Plots Generator
# -----------------------------------------------------------------------------
def plot_circuit_diagram(num_qubits):
    """
    Renders a clean, high-contrast dark quantum circuit diagram
    styled precisely after the reference design in Image 1.
    """
    fig, ax = plt.subplots(figsize=(6.8, 2.5), facecolor="#0a1222")
    ax.set_facecolor("#0a1222")

    # Qubit wire lines
    y_coords = list(range(num_qubits - 1, -1, -1))

    # Calculate horizontal span based on qubits
    total_steps = 5 if num_qubits == 2 else (3 if num_qubits == 1 else 7)
    x_max = total_steps + 0.8

    for idx, y in enumerate(y_coords):
        ax.plot([0.5, x_max], [y, y], color="#38bdf8", lw=1.6, zorder=1)
        ax.text(
            0.1,
            y,
            f"$q_{idx}$  $|0\\rangle$",
            color="#e2e8f0",
            fontsize=11,
            fontweight="bold",
            va="center",
            ha="right",
        )

    # Gate placement logic
    if num_qubits == 1:
        # 1-Qubit: H gate and Measurement
        ax.add_patch(
            patches.FancyBboxPatch(
                (1.8, -0.3),
                0.8,
                0.6,
                boxstyle="round,pad=0.08",
                facecolor="#0284c7",
                edgecolor="#38bdf8",
                lw=1.5,
                zorder=3,
            )
        )
        ax.text(2.2, 0, "H", color="white", fontsize=11, fontweight="bold", ha="center", va="center", zorder=4)

        ax.add_patch(
            patches.FancyBboxPatch(
                (3.0, -0.3),
                0.8,
                0.6,
                boxstyle="round,pad=0.08",
                facecolor="#1e293b",
                edgecolor="#475569",
                lw=1.5,
                zorder=3,
            )
        )
        ax.text(3.4, 0, "M", color="#cbd5e1", fontsize=10, fontweight="bold", ha="center", va="center", zorder=4)

    elif num_qubits == 2:
        # 2-Qubit: H, R2, SWAP, Measure matching Image 1
        # Qubit 0: H at x=1.3, R2 at x=2.3, swap dot at x=3.3, measure at x=4.8
        # Qubit 1: H at x=1.3, R2 at x=2.3, X at x=3.3, measure at x=4.8
        ax.add_patch(
            patches.FancyBboxPatch(
                (1.1, 0.7),
                0.65,
                0.6,
                boxstyle="round,pad=0.06",
                facecolor="#0284c7",
                edgecolor="#38bdf8",
                lw=1.2,
                zorder=3,
            )
        )
        ax.text(1.42, 1, "H", color="white", fontsize=11, fontweight="bold", ha="center", va="center", zorder=4)

        ax.add_patch(
            patches.FancyBboxPatch(
                (1.1, -0.3),
                0.65,
                0.6,
                boxstyle="round,pad=0.06",
                facecolor="#0284c7",
                edgecolor="#38bdf8",
                lw=1.2,
                zorder=3,
            )
        )
        ax.text(1.42, 0, "H", color="white", fontsize=11, fontweight="bold", ha="center", va="center", zorder=4)

        # R2 gates
        ax.add_patch(
            patches.FancyBboxPatch(
                (2.1, 0.7),
                0.65,
                0.6,
                boxstyle="round,pad=0.06",
                facecolor="#9333ea",
                edgecolor="#c084fc",
                lw=1.2,
                zorder=3,
            )
        )
        ax.text(2.42, 1, "$R_2$", color="white", fontsize=10, fontweight="bold", ha="center", va="center", zorder=4)

        ax.add_patch(
            patches.FancyBboxPatch(
                (2.1, -0.3),
                0.65,
                0.6,
                boxstyle="round,pad=0.06",
                facecolor="#9333ea",
                edgecolor="#c084fc",
                lw=1.2,
                zorder=3,
            )
        )
        ax.text(2.42, 0, "$R_2$", color="white", fontsize=10, fontweight="bold", ha="center", va="center", zorder=4)

        # SWAP vertical line and gates at x=3.2
        ax.plot([3.2, 3.2], [0, 1], color="#38bdf8", lw=2, zorder=2)
        ax.plot([3.2], [1], marker="o", markersize=6, color="#38bdf8", zorder=3)
        ax.plot([3.2], [0], marker="o", markersize=6, color="#38bdf8", zorder=3)

        # X gate at x=4.0 on wire 0
        ax.add_patch(
            patches.FancyBboxPatch(
                (3.8, -0.3),
                0.65,
                0.6,
                boxstyle="round,pad=0.06",
                facecolor="#db2777",
                edgecolor="#f472b6",
                lw=1.2,
                zorder=3,
            )
        )
        ax.text(4.12, 0, "X", color="white", fontsize=11, fontweight="bold", ha="center", va="center", zorder=4)

        # Measurement gates at x=4.9
        for y in [0, 1]:
            ax.add_patch(
                patches.FancyBboxPatch(
                    (4.7, y - 0.3),
                    0.65,
                    0.6,
                    boxstyle="round,pad=0.06",
                    facecolor="#1e293b",
                    edgecolor="#475569",
                    lw=1.2,
                    zorder=3,
                )
            )
            # Gauge symbol
            arc = patches.Arc((5.02, y - 0.1), 0.35, 0.3, angle=0, theta1=0, theta2=180, color="#cbd5e1", lw=1.4, zorder=4)
            ax.add_patch(arc)
            ax.plot([5.02, 5.12], [y - 0.1, y + 0.1], color="#cbd5e1", lw=1.4, zorder=4)

    else:
        # N=8 (3 Qubits): Modular multi-qubit visual representation
        for i in range(num_qubits):
            y = y_coords[i]
            # H gate
            ax.add_patch(
                patches.FancyBboxPatch(
                    (1.1 + i * 0.4, y - 0.3),
                    0.6,
                    0.6,
                    boxstyle="round,pad=0.06",
                    facecolor="#0284c7",
                    edgecolor="#38bdf8",
                    lw=1.2,
                    zorder=3,
                )
            )
            ax.text(
                1.4 + i * 0.4, y, "H", color="white", fontsize=10, fontweight="bold", ha="center", va="center", zorder=4
            )

        # R Phase block
        ax.add_patch(
            patches.FancyBboxPatch(
                (3.2, -0.3),
                1.1,
                num_qubits - 0.4,
                boxstyle="round,pad=0.08",
                facecolor="#9333ea",
                edgecolor="#c084fc",
                lw=1.2,
                zorder=3,
            )
        )
        ax.text(
            3.75,
            (num_qubits - 1) / 2,
            "$R_k$",
            color="white",
            fontsize=12,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=4,
        )

        # SWAP block
        ax.add_patch(
            patches.FancyBboxPatch(
                (4.7, -0.3),
                0.8,
                num_qubits - 0.4,
                boxstyle="round,pad=0.08",
                facecolor="#db2777",
                edgecolor="#f472b6",
                lw=1.2,
                zorder=3,
            )
        )
        ax.text(
            5.1,
            (num_qubits - 1) / 2,
            "SWAP",
            color="white",
            fontsize=9,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=4,
        )

        # Measurement gates
        for y in y_coords:
            ax.add_patch(
                patches.FancyBboxPatch(
                    (5.8, y - 0.3),
                    0.65,
                    0.6,
                    boxstyle="round,pad=0.06",
                    facecolor="#1e293b",
                    edgecolor="#475569",
                    lw=1.2,
                    zorder=3,
                )
            )
            arc = patches.Arc((6.12, y - 0.1), 0.35, 0.3, angle=0, theta1=0, theta2=180, color="#cbd5e1", lw=1.4, zorder=4)
            ax.add_patch(arc)
            ax.plot([6.12, 6.22], [y - 0.1, y + 0.1], color="#cbd5e1", lw=1.4, zorder=4)

    ax.set_xlim(-0.5, x_max + 0.5)
    ax.set_ylim(-0.7, (num_qubits - 1) + 0.7)
    ax.axis("off")
    plt.tight_layout()
    return fig


def plot_magnitude_comparison(quantum_output, expected_qft):
    """
    Renders magnitude comparison line plot matching Image 1.
    """
    n = len(quantum_output)
    indices = np.arange(n)

    fig, ax = plt.subplots(figsize=(5.5, 3.2), facecolor="#0a1222")
    ax.set_facecolor("#0a1222")

    q_mag = np.abs(quantum_output)
    c_mag = np.abs(expected_qft)

    ax.plot(
        indices,
        q_mag,
        color="#38bdf8",
        marker="o",
        markersize=6,
        linewidth=1.8,
        label="Quantum QFT",
        zorder=3,
    )
    ax.plot(
        indices,
        c_mag,
        color="#f59e0b",
        linestyle="--",
        marker="s",
        markersize=5,
        linewidth=1.8,
        label="Classical FFT (Normalized)",
        zorder=4,
    )

    ax.set_xlabel("Frequency Index", color="#94a3b8", fontsize=9, labelpad=6)
    ax.set_ylabel("Magnitude", color="#94a3b8", fontsize=9, labelpad=6)
    ax.set_xticks(indices)
    ax.tick_params(colors="#94a3b8", labelsize=8)

    ax.grid(True, color="#1e293b", linestyle="-", linewidth=0.8, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color("#1e293b")

    leg = ax.legend(
        facecolor="#0a1222",
        edgecolor="#1e293b",
        fontsize=8,
        labelcolor="#e2e8f0",
        loc="upper right",
    )
    plt.tight_layout()
    return fig


def plot_complex_components(quantum_output, expected_qft):
    """
    Renders Real and Imaginary components plot matching Image 1.
    """
    n = len(quantum_output)
    indices = np.arange(n)

    fig, ax = plt.subplots(figsize=(5.5, 3.2), facecolor="#0a1222")
    ax.set_facecolor("#0a1222")

    ax.plot(
        indices,
        quantum_output.real,
        color="#38bdf8",
        marker="o",
        markersize=5,
        linewidth=1.8,
        label="QFT Real",
        zorder=3,
    )
    ax.plot(
        indices,
        expected_qft.real,
        color="#f59e0b",
        linestyle="--",
        marker="s",
        markersize=5,
        linewidth=1.8,
        label="FFT Real (Normalized)",
        zorder=4,
    )
    ax.plot(
        indices,
        quantum_output.imag,
        color="#10b981",
        linestyle="-.",
        marker="^",
        markersize=5,
        linewidth=1.8,
        label="QFT Imaginary",
        zorder=3,
    )
    ax.plot(
        indices,
        expected_qft.imag,
        color="#c084fc",
        linestyle=":",
        marker="*",
        markersize=6,
        linewidth=1.8,
        label="FFT Imaginary (Normalized)",
        zorder=4,
    )

    ax.set_xlabel("Output Index", color="#94a3b8", fontsize=9, labelpad=6)
    ax.set_ylabel("Amplitude", color="#94a3b8", fontsize=9, labelpad=6)
    ax.set_xticks(indices)
    ax.tick_params(colors="#94a3b8", labelsize=8)

    ax.grid(True, color="#1e293b", linestyle="-", linewidth=0.8, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color("#1e293b")

    leg = ax.legend(
        facecolor="#0a1222",
        edgecolor="#1e293b",
        fontsize=7.5,
        labelcolor="#e2e8f0",
        loc="upper right",
    )
    plt.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# Sidebar: Input Signal Panel (Section A)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="font-size: 1.3rem; color: #38bdf8;">📈</span>
            <span style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 700; color: #ffffff;">Input Signal</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("Select a predefined signal or enter your own:")

    # Signal mode selection
    preset_choice = st.selectbox(
        "Signal Selection Mode",
        options=["Custom Signal", "[1, 0]  (N=2)", "[1, 0, 1, 0]  (N=4)", "[1, 2, 0, 1, 0, 1, 0, 0]  (N=8)"],
        index=0,
        label_visibility="collapsed",
    )

    # Preset mapping
    if preset_choice == "[1, 0]  (N=2)":
        default_val = "1, 0"
    elif preset_choice == "[1, 0, 1, 0]  (N=4)":
        default_val = "1, 0, 1, 0"
    elif preset_choice == "[1, 2, 0, 1, 0, 1, 0, 0]  (N=8)":
        default_val = "1, 2, 0, 1, 0, 1, 0, 0"
    else:
        default_val = "1, 0, 1, 0"

    signal_text = st.text_input(
        "Signal (comma separated values)",
        value=default_val,
        help="Enter numbers separated by commas or spaces. Length must be a power of 2.",
    )

    st.caption("Length must be a power of 2 (2, 4, 8, 16, ...).")

    # Run Analysis Button
    run_btn = st.button("▶ Run Analysis")

    st.markdown("<br>", unsafe_allow_html=True)

    # Available Test Signals Radio List (Image 1 reference)
    st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #94a3b8; margin-bottom: 6px;'>Available Test Signals</div>", unsafe_allow_html=True)
    radio_choice = st.radio(
        "Available Signals",
        options=["[1, 0]  (N=2)", "[1, 0, 1, 0]  (N=4)", "[1, 2, 0, 1, 0, 1, 0, 0]  (N=8)", "Custom Signal"],
        index=1 if preset_choice == "Custom Signal" else [" [1, 0]  (N=2)", "[1, 0, 1, 0]  (N=4)", "[1, 2, 0, 1, 0, 1, 0, 0]  (N=8)", "Custom Signal"].index(preset_choice) if preset_choice in ["[1, 0]  (N=2)", "[1, 0, 1, 0]  (N=4)", "[1, 2, 0, 1, 0, 1, 0, 0]  (N=8)"] else 3,
        label_visibility="collapsed",
    )

    # If radio changed from sidebar
    if radio_choice != preset_choice and radio_choice != "Custom Signal":
        if radio_choice == "[1, 0]  (N=2)":
            signal_text = "1, 0"
        elif radio_choice == "[1, 0, 1, 0]  (N=4)":
            signal_text = "1, 0, 1, 0"
        elif radio_choice == "[1, 2, 0, 1, 0, 1, 0, 0]  (N=8)":
            signal_text = "1, 2, 0, 1, 0, 1, 0, 0"

    st.markdown("<br>", unsafe_allow_html=True)

    # About Project Callout Card
    st.markdown(
        """
        <div class="dashboard-card" style="background: #09101f; border-color: #1a2942;">
            <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #f59e0b; font-size: 0.95rem; margin-bottom: 8px;">
                <span>💡</span> About This Project
            </div>
            <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin: 0 0 10px 0;">
                This dashboard compares the <strong>Quantum Fourier Transform (QFT)</strong> implemented in Qiskit with the classical <strong>Fast Fourier Transform (FFT)</strong> using NumPy.
            </p>
            <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.5; margin: 0;">
                You can select different input signals, view the quantum circuit, compare results, and see numerical validation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Top Navigation Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="top-header">
        <div class="header-left">
            <div class="header-logo">⚛</div>
            <div>
                <div class="header-title">QFT vs Classical FFT</div>
                <div class="header-subtitle">Comparative Study of Quantum Fourier Transform and Classical Fast Fourier Transform</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 18px;">
            <div class="header-badges">
                <span>Qiskit</span> &nbsp;|&nbsp;
                <span>NumPy</span> &nbsp;|&nbsp;
                <span>Matplotlib</span> &nbsp;|&nbsp;
                <span>Streamlit</span>
            </div>
            <div class="team-badge">
                <span>👥</span>
                <div>
                    <div style="font-size: 0.75rem; color: #94a3b8; line-height: 1;">Team Project</div>
                    <div style="font-size: 0.82rem; font-weight: 700; color: #ffffff;">3 Members</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Parse & Analyze Signal
# -----------------------------------------------------------------------------
try:
    tokens = re.split(r"[,\s]+", signal_text.strip())
    raw_values = [float(t) for t in tokens if len(t) > 0]
    results = analyze_signal(raw_values)
except Exception as exc:
    st.error(f"❌ Input Error: {exc}")
    st.stop()


# -----------------------------------------------------------------------------
# ROW 1: Quantum Circuit (B) & Validation Results (E)
# -----------------------------------------------------------------------------
col_top_left, col_top_right = st.columns([1.45, 1.0])

# --- Panel B: Quantum Circuit Panel ---
with col_top_left:
    st.markdown(
        f"""
        <div class="dashboard-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <div class="card-title" style="margin-bottom: 2px;">Quantum Circuit (QFT)</div>
                    <div style="font-size: 0.78rem; color: #94a3b8;">
                        Number of qubits: <strong style="color: #ffffff;">{results['num_qubits']}</strong> &nbsp;|&nbsp; 
                        Input length: <strong style="color: #ffffff;">{results['n']}</strong>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Render Circuit Diagram
    fig_circ = plot_circuit_diagram(results["num_qubits"])
    st.pyplot(fig_circ, use_container_width=True)
    plt.close(fig_circ)

    # Circuit Legend Badges
    st.markdown(
        """
        <div class="circuit-legend">
            <span class="legend-tag tag-h">H &nbsp;Hadamard Gate</span>
            <span class="legend-tag tag-r">R₂ &nbsp;Controlled Phase Gate</span>
            <span class="legend-tag tag-x">X &nbsp;SWAP Gate</span>
            <span class="legend-tag tag-m">⎎ &nbsp;Measurement</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Panel E: Validation and Results Panel ---
with col_top_right:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="card-title">
                <span style="color: #10b981;">✔</span> Validation Results
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Results Match Banner
    if results["is_match"]:
        st.markdown(
            """
            <div class="success-card">
                <div class="success-icon">✓</div>
                <div>
                    <div class="success-title">Results Match!</div>
                    <div class="success-desc">The quantum QFT and normalized classical FFT give nearly identical results.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="success-card" style="border-color: #f59e0b; background: rgba(245, 158, 11, 0.1);">
                <div class="success-icon" style="background: #f59e0b;">!</div>
                <div>
                    <div class="success-title" style="color: #f59e0b;">Numerical Discrepancy</div>
                    <div class="success-desc">The error exceeded tolerance threshold.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Metrics Rows
    st.markdown(
        f"""
        <div class="metric-row">
            <span class="metric-name">Maximum Absolute Error</span>
            <span class="metric-val" style="color: #38bdf8;">{results['max_error']:.4e}</span>
        </div>
        <div class="metric-row">
            <span class="metric-name">Signal Length (N)</span>
            <span class="metric-val">{results['n']}</span>
        </div>
        <div class="metric-row">
            <span class="metric-name">Number of Qubits</span>
            <span class="metric-val">{results['num_qubits']}</span>
        </div>
        <div class="metric-row">
            <span class="metric-name">Normalization Factor (1/√N)</span>
            <span class="metric-val">{results['norm_factor']:.4f}</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# ROW 2: Magnitude Comparison (C) & Real/Imaginary Components (D)
# -----------------------------------------------------------------------------
col_mid_left, col_mid_right = st.columns(2)

# --- Panel C: Magnitude Comparison ---
with col_mid_left:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="card-title">
                <span style="color: #38bdf8;">📊</span> Magnitude Comparison
            </div>
        """,
        unsafe_allow_html=True,
    )
    fig_mag = plot_magnitude_comparison(results["quantum_output"], results["expected_qft"])
    st.pyplot(fig_mag, use_container_width=True)
    plt.close(fig_mag)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Panel D: Real and Imaginary Components ---
with col_mid_right:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="card-title">
                <span style="color: #a855f7;">〰</span> Real and Imaginary Components
            </div>
        """,
        unsafe_allow_html=True,
    )
    fig_comp = plot_complex_components(results["quantum_output"], results["expected_qft"])
    st.pyplot(fig_comp, use_container_width=True)
    plt.close(fig_comp)
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Signal Values Comparison: Classical vs Quantum
# -----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
col_sig_cl, col_sig_qu = st.columns(2)

with col_sig_cl:
    sig_real_disp = (
        np.array2string(results['signal'].real, precision=3, separator=', ')
        if np.all(np.isclose(results['signal'].imag, 0))
        else np.array2string(results['signal'], precision=3, separator=', ')
    )
    fft_disp = np.array2string(results['classical_fft'], precision=3, separator=', ')
    bridge_disp = np.array2string(results['expected_qft'], precision=3, separator=', ')

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="card-title">
                <span style="color: #38bdf8;">💻</span> Classical Signal Values (NumPy)
            </div>
            <div class="metric-row">
                <span class="metric-name">Input Signal x</span>
                <span class="metric-val">{sig_real_disp}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Signal Norm ||x||₂</span>
                <span class="metric-val">{results['norm']:.4f}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Raw Classical FFT Xₖ</span>
                <span class="metric-val" style="font-size: 0.78rem;">{fft_disp}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Normalized FFT (Bridge)</span>
                <span class="metric-val" style="font-size: 0.78rem;">{bridge_disp}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_sig_qu:
    state_in_disp = np.array2string(results['normalized_signal'], precision=3, separator=', ')
    qft_out_disp = np.array2string(results['quantum_output'], precision=3, separator=', ')

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="card-title">
                <span style="color: #a855f7;">⚛</span> Quantum Signal Values (Qiskit)
            </div>
            <div class="metric-row">
                <span class="metric-name">Qubit Register Size</span>
                <span class="metric-val">{results['num_qubits']} Qubit{'s' if results['num_qubits'] > 1 else ''} (2^{results['num_qubits']} = {results['n']} basis states)</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">State Preparation |ψ_in⟩</span>
                <span class="metric-val" style="font-size: 0.78rem;">{state_in_disp}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">QFT State Amplitudes |ψ̃⟩</span>
                <span class="metric-val" style="font-size: 0.78rem;">{qft_out_disp}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Quantum-Classical Error</span>
                <span class="metric-val" style="color: #10b981;">{results['max_error']:.4e} ({'PASS' if results['is_match'] else 'CHECK'})</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# ROW 3: Numerical Results Table (F) & Key Takeaways
# -----------------------------------------------------------------------------
col_bot_left, col_bot_right = st.columns([1.6, 1.0])

# --- Panel F: Numerical Results Table ---
with col_bot_left:
    st.markdown(
        """
        <div class="dashboard-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div class="card-title" style="margin-bottom: 0;">Detailed Numerical Results Table</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Display clean table
    st.dataframe(
        results["df_results"],
        use_container_width=True,
        hide_index=True,
    )

    # Download CSV button
    csv_buffer = io.StringIO()
    results["df_results"].to_csv(csv_buffer, index=False)
    st.download_button(
        label="⤓ Download Results CSV",
        data=csv_buffer.getvalue(),
        file_name=f"qft_fft_N{results['n']}_results.csv",
        mime="text/csv",
    )

    st.markdown("</div>", unsafe_allow_html=True)

# --- Key Takeaways Card ---
with col_bot_right:
    st.markdown(
        """
        <div class="dashboard-card">
            <div class="card-title">
                <span style="color: #38bdf8;">💡</span> Key Takeaways
            </div>
            <div class="takeaway-item">
                <span class="takeaway-icon">✔</span>
                <span>QFT and classical FFT produce the same results after normalisation (up to <strong>numerical precision</strong>).</span>
            </div>
            <div class="takeaway-item">
                <span class="takeaway-icon">✔</span>
                <span>The quantum circuit uses Hadamard and controlled-phase gates to transform the state.</span>
            </div>
            <div class="takeaway-item">
                <span class="takeaway-icon">✔</span>
                <span>The number of qubits required is <strong>log₂(N)</strong>.</span>
            </div>
            <div class="takeaway-item">
                <span class="takeaway-icon">✔</span>
                <span>QFT is a quantum operation, while FFT is a classical algorithm.</span>
            </div>
            <div class="takeaway-item">
                <span class="takeaway-icon">✔</span>
                <span>QFT is useful as a subroutine in quantum algorithms, but it is <strong>not faster than classical FFT on a normal computer</strong>.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="dashboard-footer">
        <div>QFT vs Classical FFT &nbsp;|&nbsp; Quantum Computing Project</div>
        <div>Made with ❤️ using Streamlit</div>
    </div>
    """,
    unsafe_allow_html=True,
)
