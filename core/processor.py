import numpy as np
from typing import Dict

class SignalProcessor:
    @staticmethod
    def calculate_features(raw: Dict) -> Dict[str, float]:
        hrv = raw["hrv_rmssd"]
        hr = raw["hr_mean"]
        resp = raw["resp_rate"]
        
        features = {
            "hrv_log": np.log(hrv + 1),
            "normalized_hrv": (hrv - 20) / 100,
            "lf_hf_proxy": max(0.5, min(4.0, 80 / hrv)),
            "variability_index": hrv / hr if hr > 0 else 0,
            "resp_sync": 1 / (1 + np.exp(-(resp - 16))),
            "hr_stability": 1 / (1 + abs(hr - 70) / 20),
        }
        
        # Extra real-data metrics if available
        if raw.get("rr_intervals") and len(raw["rr_intervals"]) >= 5:
            rr = np.array(raw["rr_intervals"])
            features["rr_sdnn"] = float(np.std(rr))
            features["data_quality"] = 1.0
        else:
            features["data_quality"] = raw.get("signal_quality", 0.6)
            
        return features
