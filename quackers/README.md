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
└── pyproject.toml / requirements.txt     # Dependency specification
