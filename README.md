# BioSignal-Veto

## The Architecture of Sovereignty
This repository is organized into a dual-gate system to return data dignity to the body.

### 1. The Core (Sovereign Engine)
Located in `/core`, this contains the high-fidelity processing logic for the **Polar H10**. 
- **Truth Source:** Raw ECG-derived RMSSD.
- **Status:** Primary/Absolute.

### 2. The Universal Bridge (Mainstream Gate)
The `universal_gate.py` at the root acts as the listener for the **Apple Watch**.
- **Data Type:** Optical PPG "Reflection".
- **Humility Filter:** A 0.85x calibration is automatically applied to all incoming Apple Watch data to account for optical noise and algorithmic processing.

## Current Setup
- **Universal Bridge:** Listens on port `5000`.
- **Requirements:** Flask, Bleak, Numpy, Requests.
