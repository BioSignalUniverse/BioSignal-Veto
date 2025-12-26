import sys
import os
from flask import Flask, request

# Connect to your new Core folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    # Importing your engine from core/executor.py or core/main.py
    from executor import BioSignalEngine 
    print("Sovereign Engine Linked.")
except ImportError:
    print("Engine link pending—check file names in /core.")

app = Flask(__name__)

@app.route('/apple_bridge', methods=['POST'])
def apple_bridge():
    """
    The Mainstream Gate: Receives Apple Watch data via Webhook.
    Applies the 'Humility Filter' (0.85x) to account for optical noise.
    """
    data = request.json
    raw_hrv = data.get('hrv', 0)
    calibrated_hrv = raw_hrv * 0.85 
    
    print(f"Reflection Received: {calibrated_hrv} HRV (Calibrated)")
    return {"status": "success", "source": "Apple Watch"}

if __name__ == "__main__":
    # Start the bridge on port 5000
    app.run(host='0.0.0.0', port=5000)
  
