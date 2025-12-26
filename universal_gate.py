import sys
import os
import threading
from flask import Flask, request

# 1. Force the system to see your new 'core' directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    # This connects to the 'Sovereign Engine' you just moved
    from executor import BioSignalEngine 
    engine = BioSignalEngine()
    print("Sovereign Engine Linked successfully.")
except ImportError as e:
    print(f"Linkage Error: {e}. Check if 'executor.py' is in 'core' folder.")

app = Flask(__name__)

# 2. The Mainstream Gate (Apple/PPG)
@app.route('/apple_bridge', methods=['POST'])
def apple_bridge():
    """
    Receives 'The Reflection' (Apple Watch data).
    Applies the Humility Filter (0.85x) before passing to the engine.
    """
    data = request.json
    # Extract HRV (RMSSD) from the incoming JSON
    raw_hrv = data.get('hrv', 0)
    
    # Apply Humility Filter: 15% reduction for processed optical data
    calibrated_hrv = raw_hrv * 0.85 
    
    print(f"Reflection Received: {calibrated_hrv} HRV (Calibrated via Humility Filter)")
    
    # Here you would pass 'calibrated_hrv' into your engine logic
    # engine.process_external_signal(calibrated_hrv)
    
    return {"status": "Veto Logic Applied", "gate": "Mainstream"}

# 3. Running both gates simultaneously
def run_bridge():
    # Start the Sovereign Engine (Polar H10) in the background
    threading.Thread(target=engine.run, daemon=True).start()
    
    # Start the Apple Webhook Listener
    print("Universal Bridge Listening on Port 5000...")
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_bridge()
