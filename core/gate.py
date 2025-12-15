from typing import Dict, Any
import json
import os

class DecisionGate:
    def __init__(self, config_path: str = "config/thresholds.json"):
        if os.path.exists(config_path):
            with open(config_path) as f:
                cfg = json.load(f)
            self.thresholds = cfg.get("thresholds", {})
            self.weights = cfg.get("weights", {})
        else:
            # Defaults
            self.thresholds = {
                "hrv_log": 3.8, "normalized_hrv": 0.55, "lf_hf_proxy": 1.5,
                "variability_index": 0.5, "resp_sync": 0.6, "hr_stability": 0.8
            }
            self.weights = {
                "hrv_log": 0.30, "normalized_hrv": 0.25, "lf_hf_proxy": 0.20,
                "variability_index": 0.10, "resp_sync": 0.10, "hr_stability": 0.05
            }
        self.total_weight = sum(self.weights.values())
        self.decision_threshold = 0.7
    
    def evaluate(self, features: Dict[str, float], raw: Dict) -> Dict[str, Any]:
        score = 0.0
        details = {}
        
        for feat, value in features.items():
            if feat in self.thresholds and feat in self.weights:
                thresh = self.thresholds[feat]
                weight = self.weights[feat]
                met = value >= thresh
                if met:
                    score += weight
                details[feat] = {"value": round(value, 3), "threshold": thresh, "met": met}
        
        normalized_score = score / self.total_weight if self.total_weight > 0 else 0
        
        veto_eligible = False
        if raw.get("data_source") == "POLAR_H10_REAL":
            if features.get("hrv_log", 0) > 4.0 and features.get("lf_hf_proxy", 3) < 2.0 and raw.get("hr_mean", 100) < 80:
                veto_eligible = True
        
        proceed = normalized_score >= self.decision_threshold
        
        return {
            "decision": "PROCEED" if proceed else "WAIT",
            "score": round(normalized_score, 3),
            "veto_eligible": veto_eligible,
            "veto_status": "ARMED" if veto_eligible else "STANDBY",
            "details": details,
            "features": features
              }
