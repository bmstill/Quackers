# CU to CZ: From Zero to Quero

**QuEra Creator’s Challenge — iQuHACK 2026**
**Team Quackers:** Kai Tucker, Nadia Chestnut, Julia Holzbach, Bryson Still
[Challenge Description](https://github.com/iQuHACK/2026-QuEra-Creator/tree/main)

---

## Project Overview

This project presents a **visual narrative of the controlled-Z (CZ) gate** on neutral-atom quantum computers. Rather than depicting the CZ gate as an abstract circuit primitive, we visualize how entanglement emerges from **laser-driven Rydberg dynamics and conditional phase accumulation**.

Through synchronized animations—energy-level diagrams and Bloch-sphere trajectories—we explicitly show:
- Continuous phase accumulation during the gate pulse
- State-dependent dynamics of \(|01⟩\) versus \(|11⟩\)
- The role of Rydberg blockade in generating the entangling \(−\pi\) phase
- How computational states return to themselves in population while still becoming entangled

The goal is to bridge the gap between **circuit-level abstractions** and the **physical reality of neutral-atom hardware**, in alignment with the QuEra Creator’s Challenge emphasis on clarity, correctness, and reproducibility.

---

## Repository Structure

The repository is organized to separate **physics simulation**, **animation logic**, and **documentation**:

```text
.
├── SingleQubitEvolution.py        # QuTiP simulation of single-qubit phase evolution
├── MultiQubitEvolution.py         # Two-qubit Hamiltonian evolution (CZ dynamics)
├── ket10.py                       # Animation logic for |01⟩ / |10⟩ phase evolution
├── ket11.py                       # Animation logic for |11⟩ phase evolution under blockade
├── README.md                      # Project overview and reproduction instructions
├── documentation/
│   └── CU_to_CZ_From_Zero_to_Quero.pdf   # Full technical write-up / judging guide
├── presentation/
│   └── CU_to_CZ_Presentation.pdf         # iQuHACK presentation slides
├── assets/
│   ├── single_qubit_phase.gif
│   ├── energy_level_dynamics.gif
│   └── bloch_sphere_cz.gif
```

## Model (hardware-faithful, simplified)

We evolve the quantum states using a simplified two-atom Hamiltonian that captures the essential physics of a neutral-atom controlled-Z (CZ) gate mediated by Rydberg blockade:

\[
H(t) = \sum_{i=1}^{2}\left[\frac{\Omega(t)}{2}\left(|r⟩⟨1|_i + |1⟩⟨r|_i\right) - \Delta(t)|r⟩⟨r|_i\right] + V |rr⟩⟨rr|
\]

where:

- \(\Omega(t)\) is the effective Raman Rabi frequency coupling the \(|1⟩\) ground state to the Rydberg state \(|r⟩\)
- \(\Delta(t)\) is the laser detuning
- \(V\) is the Rydberg–Rydberg interaction energy responsible for blockade

This Hamiltonian naturally separates the dynamics into distinct subspaces:

- States \(|01⟩\) and \(|10⟩\) evolve as effectively single-atom driven systems and acquire **single-qubit Z phases**
- The \(|11⟩\) state experiences an interaction-shifted energy landscape, leading to **additional conditional phase accumulation**

All computational basis states return to themselves in population at the end of the pulse, but with different accumulated phases. The relative \(-\pi\) phase on \(|11⟩\) constitutes the entangling resource of the CZ gate, defined up to local Z rotations.

---

## Reproducibility

All simulations and animations in this project are generated programmatically. The following steps reproduce the full pipeline from numerical evolution to rendered animations.

### 1. Environment setup

**Python 3.10+ recommended**

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows PowerShell
python -m pip install --upgrade pip
```

