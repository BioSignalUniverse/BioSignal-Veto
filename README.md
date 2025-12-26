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




​🛠 Technical FAQ: Connecting to the Bridge
​1. I’m on an older iPhone/OS; will the Shortcut work?
​Yes. The Apple Shortcut "Post" method uses standard web protocols. As long as your iOS version supports the Shortcuts app and "Get Contents of URL," you can flow data to the bridge.
​2. How do I find my server IP?
​If you are running universal_gate.py on a laptop at home, your phone must be on the same Wi-Fi.
​Find IP: Run ipconfig (Windows) or ifconfig (Mac/Linux) in your terminal.
​The Bridge: Enter that IP followed by :5000/apple_bridge in your Shortcut URL field.
​3. Why the 0.85x "Humility Filter"?
​We use this to account for the physical difference in sensors:
​The Constant (Core): Polar H10 measures electrical heart signals (ECG).
​The Reflection (Bridge): Apple Watch measures light-based pulse (PPG).
​The Math: The 15% reduction (0.85x) is a coded "Veto" against the inherent noise and smoothing often found in optical sensors.
​4. My data isn't showing up. What do I check?
​Requirements: Ensure flask is installed via your updated requirements.txt.
​Listener: Make sure universal_gate.py is actually running and shows "Listening on Port 5000".
​Bypass: Confirm you are working on the main branch, as the Sovereign Bypass we established ensures your updates are live.

