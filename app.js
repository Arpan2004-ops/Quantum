/**
 * QFT vs Classical FFT - Interactive Dashboard Application Logic
 */

// Ground-truth experiment data from results/
const EXPERIMENT_DATA = {
  experiment_1: {
    id: "experiment_1",
    name: "Experiment 1 (N = 2)",
    input_str: "[1, 0]",
    input_raw: [1, 0],
    n: 2,
    qubits: 1,
    max_error: 0.0,
    validation: "PASS",
    classical_time: "0.02319730 s",
    quantum_time: "0.00516800 s",
    circuit_img: "./results/experiment_1_circuit.png",
    circuit_txt: `     ┌────────────────────────┐┌──────┐
q_0: ┤0                       ├┤0     ├
     │  State Preparation(1,0) ││  Qft │
     └────────────────────────┘└──────┘`,
    magnitude_img: "./results/experiment_1_magnitude.png",
    complex_img: "./results/experiment_1_complex.png",
    rows: [
      { index: 0, input: "1.00000 + 0.00000j", classical_fft: "1.00000 + 0.00000j", qft_amp: "0.70711 + 0.00000j", expected_qft: "0.70711 + 0.00000j", abs_err: "0.000e+00" },
      { index: 1, input: "0.00000 + 0.00000j", classical_fft: "1.00000 + 0.00000j", qft_amp: "0.70711 + 0.00000j", expected_qft: "0.70711 + 0.00000j", abs_err: "0.000e+00" }
    ],
    log: `Experiment: experiment_1
Input signal: [1.+0.j 0.+0.j]
Number of input values: 2
Number of qubits: 1

Classical FFT: [1.+0.j 1.+0.j]
QFT amplitudes: [0.707107+0.j 0.707107+0.j]
Expected QFT amplitudes: [0.707107+0.j 0.707107+0.j]

Maximum absolute error: 0
Validation: PASS
Classical FFT wall-clock time: 0.02319730 seconds
Statevector simulation wall-clock time: 0.00516800 seconds

Validation Note: Perfect match. State preparation places qubit in |0>; QFT acts as a Hadamard gate H, yielding equal superposition (|0> + |1>)/√2.`
  },

  experiment_2: {
    id: "experiment_2",
    name: "Experiment 2 (N = 4)",
    input_str: "[1, 0, 1, 0]",
    input_raw: [1, 0, 1, 0],
    n: 4,
    qubits: 2,
    max_error: 1.40800392604e-16,
    validation: "PASS",
    classical_time: "0.00029550 s",
    quantum_time: "0.00690620 s",
    circuit_img: "./results/experiment_2_circuit.png",
    circuit_txt: `     ┌─────────────────────────────────────────┐┌──────┐
q_0: ┤0                                        ├┤0     ├
     │  State Preparation(0.70711,0,0.70711,0) ││  Qft │
q_1: ┤1                                        ├┤1     ├
     └─────────────────────────────────────────┘└──────┘`,
    magnitude_img: "./results/experiment_2_magnitude.png",
    complex_img: "./results/experiment_2_complex.png",
    rows: [
      { index: 0, input: "1.00000 + 0.00000j", classical_fft: "2.00000 + 0.00000j", qft_amp: "0.70711 + 0.00000j", expected_qft: "0.70711 + 0.00000j", abs_err: "0.000e+00" },
      { index: 1, input: "0.00000 + 0.00000j", classical_fft: "0.00000 + 0.00000j", qft_amp: "0.00000 + 4.330e-17j", expected_qft: "0.00000 + 0.00000j", abs_err: "4.330e-17" },
      { index: 2, input: "1.00000 + 0.00000j", classical_fft: "2.00000 + 0.00000j", qft_amp: "0.70711 - 8.660e-17j", expected_qft: "0.70711 + 0.00000j", abs_err: "8.660e-17" },
      { index: 3, input: "0.00000 + 0.00000j", classical_fft: "0.00000 + 0.00000j", qft_amp: "0.00000 + 1.299e-16j", expected_qft: "0.00000 + 0.00000j", abs_err: "1.299e-16" }
    ],
    log: `Experiment: experiment_2
Input signal: [1.+0.j 0.+0.j 1.+0.j 0.+0.j]
Number of input values: 4
Number of qubits: 2

Classical FFT: [2.+0.j 0.+0.j 2.+0.j 0.+0.j]
QFT amplitudes: [0.707107+0.j 0.+4.330e-17j 0.707107-8.660e-17j 0.+1.299e-16j]
Expected QFT amplitudes: [0.707107+0.j 0.+0.j 0.707107+0.j 0.+0.j]

Maximum absolute error: 1.40800392604e-16
Validation: PASS
Classical FFT wall-clock time: 0.00029550 seconds
Statevector simulation wall-clock time: 0.00690620 seconds

Validation Note: Periodic alternating input with frequency peak at k=0 and k=2. QFT output reproduces constructive interference at states |00> and |10> with amplitude 1/√2 each.`
  },

  experiment_3: {
    id: "experiment_3",
    name: "Experiment 3 (N = 8)",
    input_str: "[1, 2, 0, 1, 0, 1, 0, 0]",
    input_raw: [1, 2, 0, 1, 0, 1, 0, 0],
    n: 8,
    qubits: 3,
    max_error: 5.0267485386e-16,
    validation: "PASS",
    classical_time: "0.00033630 s",
    quantum_time: "0.00458200 s",
    circuit_img: "./results/experiment_3_circuit.png",
    circuit_txt: `     ┌────────────────────────────────────────────────────────┐┌──────┐
q_0: ┤0                                                       ├┤0     ├
     │                                                        ││      │
q_1: ┤1 State Preparation(0.37796,0.75593,0,0.37796,0,0.37796)├┤1 Qft ├
     │                                                        ││      │
q_2: ┤2                                                       ├┤2     ├
     └────────────────────────────────────────────────────────┘└──────┘`,
    magnitude_img: "./results/experiment_3_magnitude.png",
    complex_img: "./results/experiment_3_complex.png",
    rows: [
      { index: 0, input: "1.00000 + 0.00000j", classical_fft: "5.00000 + 0.00000j", qft_amp: "0.66815 - 9.00e-17j", expected_qft: "0.66815 + 0.00000j", abs_err: "8.996e-17" },
      { index: 1, input: "2.00000 + 0.00000j", classical_fft: "1.00000 - 1.41421j", qft_amp: "0.13363 + 0.18898j", expected_qft: "0.13363 + 0.18898j", abs_err: "5.551e-17" },
      { index: 2, input: "0.00000 + 0.00000j", classical_fft: "1.00000 - 2.00000j", qft_amp: "0.13363 + 0.26726j", expected_qft: "0.13363 + 0.26726j", abs_err: "2.776e-17" },
      { index: 3, input: "1.00000 + 0.00000j", classical_fft: "1.00000 - 1.41421j", qft_amp: "0.13363 + 0.18898j", expected_qft: "0.13363 + 0.18898j", abs_err: "5.551e-17" },
      { index: 4, input: "0.00000 + 0.00000j", classical_fft: "-3.00000 + 0.00000j", qft_amp: "-0.40089 + 3.40e-16j", expected_qft: "-0.40089 + 0.00000j", abs_err: "3.398e-16" },
      { index: 5, input: "1.00000 + 0.00000j", classical_fft: "1.00000 + 1.41421j", qft_amp: "0.13363 - 0.18898j", expected_qft: "0.13363 - 0.18898j", abs_err: "5.027e-16" },
      { index: 6, input: "0.00000 + 0.00000j", classical_fft: "1.00000 + 2.00000j", qft_amp: "0.13363 - 0.26726j", expected_qft: "0.13363 - 0.26726j", abs_err: "1.110e-16" },
      { index: 7, input: "0.00000 + 0.00000j", classical_fft: "1.00000 + 1.41421j", qft_amp: "0.13363 - 0.18898j", expected_qft: "0.13363 - 0.18898j", abs_err: "5.027e-16" }
    ],
    log: `Experiment: experiment_3
Input signal: [1.+0.j 2.+0.j 0.+0.j 1.+0.j 0.+0.j 1.+0.j 0.+0.j 0.+0.j]
Number of input values: 8
Number of qubits: 3

Classical FFT: [ 5.+0.j 1.-1.414214j 1.-2.j 1.-1.414214j -3.+0.j 1.+1.414214j 1.+2.j 1.+1.414214j]
QFT amplitudes: [ 0.668153-9.0e-17j  0.133631+0.188982j  0.133631+0.267261j ... ]
Expected QFT amplitudes: [ 0.668153+0.j  0.133631+0.188982j  0.133631+0.267261j ... ]

Maximum absolute error: 5.0267485386e-16
Validation: PASS
Classical FFT wall-clock time: 0.00033630 seconds
Statevector simulation wall-clock time: 0.00458200 seconds

Validation Note: Non-trivial asymmetric 8-element signal. Notice conjugate symmetry: index 1 and index 7, index 2 and index 6 have conjugate phases (identical real part, opposite imaginary sign). QFT amplitudes match with error ~ 10^-16.`
  }
};

let currentExperimentId = "experiment_2";
let simChartType = "magnitude";

// Initialize Dashboard
document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initExperimentSwitcher();
  initCircuitToggle();
  initModal();
  initSimulator();
  initVivaCards();
  renderExperiment(currentExperimentId);
});

// Tab Navigation
function initTabs() {
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTab = btn.getAttribute("data-tab");

      tabButtons.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      const targetContent = document.getElementById(targetTab);
      if (targetContent) {
        targetContent.classList.add("active");
      }

      if (targetTab === "tab-simulator") {
        updateSimulator();
      }
    });
  });
}

// Experiment Switcher
function initExperimentSwitcher() {
  const pills = document.querySelectorAll(".exp-pill");
  pills.forEach(pill => {
    pill.addEventListener("click", () => {
      pills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentExperimentId = pill.getAttribute("data-exp");
      renderExperiment(currentExperimentId);
    });
  });
}

function renderExperiment(expId) {
  const exp = EXPERIMENT_DATA[expId];
  if (!exp) return;

  // Update Metadata
  document.getElementById("meta-input").textContent = exp.input_str;
  document.getElementById("meta-size").textContent = `${exp.n} elements`;
  document.getElementById("meta-qubits").textContent = `${exp.qubits} qubits`;
  document.getElementById("meta-error").textContent = exp.max_error === 0 ? "0.000e+00" : exp.max_error.toExponential(3);
  document.getElementById("meta-validation").textContent = exp.validation;
  document.getElementById("meta-cl-time").textContent = exp.classical_time;
  document.getElementById("meta-q-time").textContent = exp.quantum_time;

  // Update Visuals
  const circuitImg = document.getElementById("exp-circuit-img");
  const circuitTxt = document.getElementById("exp-circuit-txt");
  const magImg = document.getElementById("exp-mag-img");
  const complexImg = document.getElementById("exp-complex-img");

  circuitImg.src = exp.circuit_img;
  circuitTxt.textContent = exp.circuit_txt;
  magImg.src = exp.magnitude_img;
  complexImg.src = exp.complex_img;

  // Update Data Table
  const tbody = document.getElementById("exp-table-body");
  tbody.innerHTML = "";
  exp.rows.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>|${decToBin(r.index, exp.qubits)}⟩</strong> (${r.index})</td>
      <td>${r.input}</td>
      <td>${r.classical_fft}</td>
      <td style="color: var(--cyan-primary);">${r.qft_amp}</td>
      <td style="color: var(--violet-primary);">${r.expected_qft}</td>
      <td style="color: var(--emerald-success);">${r.abs_err}</td>
      <td><span class="badge-pass">PASS</span></td>
    `;
    tbody.appendChild(tr);
  });

  // Update Log
  document.getElementById("exp-terminal-log").textContent = exp.log;
}

function decToBin(dec, bits) {
  return dec.toString(2).padStart(bits, "0");
}

// Circuit Text/Image toggle
function initCircuitToggle() {
  const btnToggle = document.getElementById("btn-toggle-circuit-view");
  const circuitImg = document.getElementById("exp-circuit-img");
  const circuitTxt = document.getElementById("exp-circuit-txt");

  if (!btnToggle) return;

  btnToggle.addEventListener("click", () => {
    if (circuitTxt.classList.contains("active")) {
      circuitTxt.classList.remove("active");
      circuitImg.style.display = "block";
      btnToggle.textContent = "View ASCII";
    } else {
      circuitTxt.classList.add("active");
      circuitImg.style.display = "none";
      btnToggle.textContent = "View Image";
    }
  });
}

// Modal Lightbox
function initModal() {
  const modal = document.getElementById("image-modal");
  const modalImg = document.getElementById("modal-img");
  const modalClose = document.getElementById("modal-close");

  document.querySelectorAll(".zoomable-img").forEach(img => {
    img.addEventListener("click", () => {
      modalImg.src = img.src;
      modal.classList.add("active");
    });
  });

  modalClose.addEventListener("click", () => {
    modal.classList.remove("active");
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("active");
    }
  });
}

// Viva Flashcard Accordion
function initVivaCards() {
  document.querySelectorAll(".viva-header").forEach(header => {
    header.addEventListener("click", () => {
      const card = header.parentElement;
      card.classList.toggle("open");
      const icon = header.querySelector(".viva-icon");
      if (icon) {
        icon.textContent = card.classList.contains("open") ? "▲" : "▼";
      }
    });
  });
}

// CSV Summary Download
function downloadCSV() {
  const csvContent = `experiment,input_size,qubits,max_absolute_error,validation,classical_seconds,statevector_seconds
experiment_1,2,1,0,PASS,0.02319730,0.00516800
experiment_2,4,2,1.40800392604e-16,PASS,0.00029550,0.00690620
experiment_3,8,3,5.0267485386e-16,PASS,0.00033630,0.00458200`;

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  const url = URL.createObjectURL(blob);
  link.setAttribute("href", url);
  link.setAttribute("download", "qft_fft_summary.csv");
  link.style.visibility = "hidden";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// -------------------------------------------------------------
// Interactive Live Quantum & Classical Simulator in JS
// -------------------------------------------------------------

function initSimulator() {
  const presetButtons = document.querySelectorAll(".preset-btn");
  const inputEl = document.getElementById("sim-signal-input");
  const chartTypeSelect = document.getElementById("sim-chart-type");

  presetButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      presetButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      inputEl.value = btn.getAttribute("data-preset");
      updateSimulator();
    });
  });

  inputEl.addEventListener("input", () => {
    presetButtons.forEach(b => b.classList.remove("active"));
    updateSimulator();
  });

  if (chartTypeSelect) {
    chartTypeSelect.addEventListener("change", (e) => {
      simChartType = e.target.value;
      updateSimulator();
    });
  }

  updateSimulator();
}

// Complex Number Helper
class Complex {
  constructor(re = 0, im = 0) {
    this.re = re;
    this.im = im;
  }
  add(c) { return new Complex(this.re + c.re, this.im + c.im); }
  sub(c) { return new Complex(this.re - c.re, this.im - c.im); }
  mul(c) {
    return new Complex(
      this.re * c.re - this.im * c.im,
      this.re * c.im + this.im * c.re
    );
  }
  scale(s) { return new Complex(this.re * s, this.im * s); }
  abs() { return Math.hypot(this.re, this.im); }
  phase() { return Math.atan2(this.im, this.re); }
  toString(prec = 4) {
    const s = this.im >= 0 ? "+" : "-";
    return `${this.re.toFixed(prec)} ${s} ${Math.abs(this.im).toFixed(prec)}j`;
  }
}

// Classical DFT/FFT (negative exponent: e^{-2pi i j k / N})
function computeClassicalFFT(x) {
  const N = x.length;
  const out = [];
  for (let k = 0; k < N; k++) {
    let sum = new Complex(0, 0);
    for (let j = 0; j < N; j++) {
      const angle = -2 * Math.PI * j * k / N;
      const w = new Complex(Math.cos(angle), Math.sin(angle));
      sum = sum.add(x[j].mul(w));
    }
    out.push(sum);
  }
  return out;
}

// Classical Inverse FFT (positive exponent: (1/N) * e^{+2pi i j k / N})
function computeClassicalIFFT(x) {
  const N = x.length;
  const out = [];
  for (let k = 0; k < N; k++) {
    let sum = new Complex(0, 0);
    for (let j = 0; j < N; j++) {
      const angle = 2 * Math.PI * j * k / N;
      const w = new Complex(Math.cos(angle), Math.sin(angle));
      sum = sum.add(x[j].mul(w));
    }
    out.push(sum.scale(1 / N));
  }
  return out;
}

// QFT Gate on normalized state vector: (1/sqrt(N)) * sum e^{+2pi i j k / N}
function computeQFT(normX) {
  const N = normX.length;
  const out = [];
  const factor = 1 / Math.sqrt(N);
  for (let k = 0; k < N; k++) {
    let sum = new Complex(0, 0);
    for (let j = 0; j < N; j++) {
      const angle = 2 * Math.PI * j * k / N;
      const w = new Complex(Math.cos(angle), Math.sin(angle));
      sum = sum.add(normX[j].mul(w));
    }
    out.push(sum.scale(factor));
  }
  return out;
}

function updateSimulator() {
  const inputEl = document.getElementById("sim-signal-input");
  const errorAlert = document.getElementById("sim-error-alert");
  const rawStr = inputEl.value.trim();

  // Parse input
  const tokens = rawStr.split(/[\s,]+/).filter(t => t.length > 0);
  const values = tokens.map(t => parseFloat(t)).filter(v => !isNaN(v));

  const N = values.length;
  const isPowerOfTwo = N >= 2 && (N & (N - 1)) === 0;

  if (!isPowerOfTwo) {
    errorAlert.style.display = "block";
    errorAlert.textContent = `Error: Input length must be a power of 2 (currently ${N}). Try length 2, 4, 8, or 16.`;
    return;
  }

  // Calculate norm
  let sumSq = 0;
  values.forEach(v => sumSq += v * v);
  const norm = Math.sqrt(sumSq);

  if (norm < 1e-12) {
    errorAlert.style.display = "block";
    errorAlert.textContent = "Error: Input signal cannot be all zeros.";
    return;
  }

  errorAlert.style.display = "none";

  const numQubits = Math.round(Math.log2(N));
  const complexSignal = values.map(v => new Complex(v, 0));
  const normalizedSignal = complexSignal.map(c => c.scale(1 / norm));

  // Run transforms
  const classicalFFT = computeClassicalFFT(complexSignal);
  const qftAmplitudes = computeQFT(normalizedSignal);

  // Expected QFT using convention bridge: sqrt(N) * IFFT(x) / norm
  const ifft = computeClassicalIFFT(complexSignal);
  const bridgeFactor = Math.sqrt(N) / norm;
  const expectedQFT = ifft.map(c => c.scale(bridgeFactor));

  // Compute error
  let maxAbsError = 0;
  for (let k = 0; k < N; k++) {
    const diff = qftAmplitudes[k].sub(expectedQFT[k]).abs();
    if (diff > maxAbsError) maxAbsError = diff;
  }

  // Update simulator stats
  document.getElementById("sim-stat-n").textContent = N;
  document.getElementById("sim-stat-qubits").textContent = numQubits;
  document.getElementById("sim-stat-norm").textContent = norm.toFixed(5);
  document.getElementById("sim-stat-error").textContent = maxAbsError.toExponential(3);
  document.getElementById("sim-stat-validation").textContent = maxAbsError < 1e-8 ? "PASS" : "CHECK";

  // Update simulator explanation text
  document.getElementById("sim-explanation").innerHTML = `
    <strong>Transformation Bridge:</strong> Input vector was normalized by $||x|| = ${norm.toFixed(4)}$.<br>
    QFT uses positive exponent $e^{+2\\pi i jk / ${N}}$ with $1/\\sqrt{${N}}$ factor. Classical forward FFT uses negative exponent $e^{-2\\pi i jk / ${N}}$.<br>
    The mathematical bridge $\\text{QFT}(x) = \\frac{\\sqrt{${N}}}{||x||_2} \\text{IFFT}(x)$ yields maximum absolute error <strong>${maxAbsError.toExponential(3)}</strong>.
  `;

  // Draw Simulator Bar Chart
  drawSimCanvas(qftAmplitudes, expectedQFT, classicalFFT, N, numQubits);

  // Draw Phasor Diagram
  drawPhasorCanvas(qftAmplitudes, N);
}

function drawSimCanvas(qft, expected, classical, N, qubits) {
  const canvas = document.getElementById("sim-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width = canvas.parentElement.clientWidth - 32;
  const h = canvas.height = 280;

  ctx.clearRect(0, 0, w, h);

  const padding = { top: 30, right: 30, bottom: 50, left: 60 };
  const plotW = w - padding.left - padding.right;
  const plotH = h - padding.top - padding.bottom;

  // Determine max value for Y-axis
  let maxVal = 0.01;
  for (let i = 0; i < N; i++) {
    const val = simChartType === "magnitude" 
      ? Math.max(qft[i].abs(), expected[i].abs())
      : Math.max(Math.abs(qft[i].re), Math.abs(qft[i].im));
    if (val > maxVal) maxVal = val;
  }
  maxVal = maxVal * 1.25;

  // Draw Grid & Axes
  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;
  const yTicks = 4;
  for (let i = 0; i <= yTicks; i++) {
    const y = padding.top + (plotH / yTicks) * i;
    ctx.beginPath();
    ctx.moveTo(padding.left, y);
    ctx.lineTo(w - padding.right, y);
    ctx.stroke();

    const labelVal = maxVal * (1 - i / yTicks);
    ctx.fillStyle = "#64748b";
    ctx.font = "10px JetBrains Mono";
    ctx.textAlign = "right";
    ctx.fillText(labelVal.toFixed(2), padding.left - 8, y + 4);
  }

  // Draw Bars / Points
  const barGroupWidth = plotW / N;
  const barWidth = Math.min(24, barGroupWidth * 0.35);

  for (let i = 0; i < N; i++) {
    const xCenter = padding.left + i * barGroupWidth + barGroupWidth / 2;

    if (simChartType === "magnitude") {
      // QFT Bar
      const qftH = (qft[i].abs() / maxVal) * plotH;
      const qftY = padding.top + plotH - qftH;
      ctx.fillStyle = "rgba(56, 189, 248, 0.85)";
      ctx.fillRect(xCenter - barWidth - 2, qftY, barWidth, qftH);

      // Expected Bar
      const expH = (expected[i].abs() / maxVal) * plotH;
      const expY = padding.top + plotH - expH;
      ctx.fillStyle = "rgba(168, 85, 247, 0.75)";
      ctx.fillRect(xCenter + 2, expY, barWidth, expH);
    } else {
      // Real component
      const reVal = qft[i].re;
      const reH = (Math.abs(reVal) / maxVal) * plotH;
      const reY = padding.top + plotH - reH;
      ctx.fillStyle = reVal >= 0 ? "rgba(56, 189, 248, 0.85)" : "rgba(244, 63, 94, 0.85)";
      ctx.fillRect(xCenter - barWidth - 2, reY, barWidth, reH);

      // Imaginary component
      const imVal = qft[i].im;
      const imH = (Math.abs(imVal) / maxVal) * plotH;
      const imY = padding.top + plotH - imH;
      ctx.fillStyle = imVal >= 0 ? "rgba(168, 85, 247, 0.85)" : "rgba(245, 158, 11, 0.85)";
      ctx.fillRect(xCenter + 2, imY, barWidth, imH);
    }

    // X Axis Labels
    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px JetBrains Mono";
    ctx.textAlign = "center";
    ctx.fillText(`|${decToBin(i, qubits)}⟩`, xCenter, h - padding.bottom + 18);
    ctx.fillStyle = "#64748b";
    ctx.font = "9px Outfit";
    ctx.fillText(`k=${i}`, xCenter, h - padding.bottom + 32);
  }

  // Legend
  ctx.textAlign = "left";
  ctx.font = "11px Outfit";
  if (simChartType === "magnitude") {
    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(w - 240, 10, 12, 12);
    ctx.fillText("Quantum QFT Amplitude", w - 222, 20);

    ctx.fillStyle = "#a855f7";
    ctx.fillRect(w - 100, 10, 12, 12);
    ctx.fillText("FFT Equivalent", w - 82, 20);
  } else {
    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(w - 220, 10, 12, 12);
    ctx.fillText("Real Part", w - 202, 20);

    ctx.fillStyle = "#a855f7";
    ctx.fillRect(w - 100, 10, 12, 12);
    ctx.fillText("Imag Part", w - 82, 20);
  }
}

// Polar Phasor Diagram (Argand Complex Plane)
function drawPhasorCanvas(qft, N) {
  const canvas = document.getElementById("phasor-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const size = Math.min(canvas.parentElement.clientWidth - 32, 280);
  canvas.width = size;
  canvas.height = size;

  const cx = size / 2;
  const cy = size / 2;
  const radius = size * 0.4;

  ctx.clearRect(0, 0, size, size);

  // Unit circle & axes
  ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(cx - radius - 15, cy);
  ctx.lineTo(cx + radius + 15, cy);
  ctx.moveTo(cx, cy - radius - 15);
  ctx.lineTo(cx, cy + radius + 15);
  ctx.stroke();

  // Axis labels
  ctx.fillStyle = "#64748b";
  ctx.font = "10px JetBrains Mono";
  ctx.textAlign = "center";
  ctx.fillText("+Re", cx + radius + 14, cy - 4);
  ctx.fillText("+Im", cx + 14, cy - radius - 4);

  // Find max magnitude
  let maxMag = 0.001;
  qft.forEach(c => {
    if (c.abs() > maxMag) maxMag = c.abs();
  });

  const colors = ["#38bdf8", "#a855f7", "#10b981", "#f59e0b", "#f43f5e", "#06b6d4", "#eab308", "#8b5cf6"];

  // Draw Phasors
  qft.forEach((c, idx) => {
    const mag = c.abs();
    if (mag < 1e-6) return;

    const len = (mag / maxMag) * radius;
    const angle = c.phase();
    const px = cx + len * Math.cos(angle);
    const py = cy - len * Math.sin(angle); // Invert Y for canvas

    const color = colors[idx % colors.length];

    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(px, py);
    ctx.stroke();

    // Arrowhead
    const headLen = 6;
    const arrowAngle = Math.atan2(cy - py, px - cx);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(px, py, 3.5, 0, 2 * Math.PI);
    ctx.fill();

    // Basis label
    ctx.fillStyle = color;
    ctx.font = "9px JetBrains Mono";
    ctx.textAlign = "center";
    ctx.fillText(`k=${idx}`, px + Math.cos(angle) * 12, py - Math.sin(angle) * 12 + 3);
  });
}
