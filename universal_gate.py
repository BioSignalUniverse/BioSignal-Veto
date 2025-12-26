import sys
import os
from flask import Flask, request, jsonify

# 1. Point to your Core folder structure
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    # This connects to the sovereign logic in your /core directory
    from executor import BioSignalEngine 
    engine = BioSignalEngine()
    print("Sovereign Engine Linked.")
except ImportError as e:
    print(f"Connection pending: {e}")

app = Flask(__name__)

# 2. The Mainstream Gate (Apple/PPG)
@app.route('/apple_bridge', methods=['POST'])
def apple_bridge():
    """
    Receives the 'Reflection' from the Apple Watch.
    Applies the Humility Filter (0.85x).
    """
    data = request.json
    raw_hrv = data.get('hrv', 0)
    
    # Applying the Humility Filter (0.85x) for the Apple 'Reflection'
    calibrated_hrv = raw_hrv * 0.85 
    
    print(f"Reflection Received: {calibrated_hrv} HRV (Calibrated)")
    
    # Return a message of success back to the iPhone screen
    return jsonify({
        "status": "Sovereignty Confirmed",
        "filter": "0.85x Humility Applied",
        "value": calibrated_hrv
    }), 200

if __name__ == "__main__":
    # Start the bridge on your local network
    print("Universal Bridge active. Awaiting handshake...")
    app.run(host='0.0.0.0', port=5000)
