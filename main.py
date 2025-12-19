import asyncio
import json
import os
from datetime import datetime
from core.sensor import PolarH10Sensor
from core.processor import SignalProcessor
from core.gate import DecisionGate
from core.executor import ActionExecutor

class BioSignalVeto:
    def __init__(self):
        self.sensor = PolarH10Sensor()
        self.processor = SignalProcessor()
        self.gate = DecisionGate()
        self.executor = ActionExecutor()
        self.veto_armed = False
        self.consecutive = 0
    
    async def initialize(self):
        print("\n" + "="*60)
        print("BIOSIGNAL VETO GATE v1.1 — PURGE PROTOCOL ENGAGED")
        print("="*60)
        
        # THE PURGE: Clean the environment before starting
        if os.path.exists("VETO_ACTIVE.lock"):
            os.remove("VETO_ACTIVE.lock")
            print("Purge: Old Veto Lock cleared.")
        
        connected = await self.sensor.discover_and_connect()
        print("REAL SENSOR ACTIVE" if connected else "SIMULATION MODE")
    
    async def run_cycle(self, cycle_id: int):
        print(f"\nCycle {cycle_id} — Measuring biosignals")
        raw = await self.sensor.measure()
        
        if raw.get("signal_quality", 0) < 0.7:
            print("Signal quality low — cycle discarded")
            return None
        
        features = self.processor.calculate_features(raw)
        # DecisionGate uses the Sovereign 0.85 threshold
        decision = self.gate.evaluate(features, raw)
        
        print(f"Score: {decision['score']:.3f} → {decision['decision']}")
        
        # Veto Logic: STABLE & USEFUL
        # Requires 2 consecutive cycles of incoherence to arm
        if decision.get("veto_eligible", False):
            self.consecutive += 1
            print(f"Incoherence detected. Warning level: {self.consecutive}/2")
            if self.consecutive >= 2 and not self.veto_armed:
                await self.executor.execute("veto_arm")
                self.veto_armed = True
        else:
            # RESET on any coherent breath
            self.consecutive = 0
            if self.veto_armed:
                await self.executor.execute("veto_release")
                self.veto_armed = False
        
        # Determine Receptivity for machine feedback
        level = decision.get("receptivity_state", {}).get("level", "UNKNOWN")
        if level == "LOW":
            print(">>> STATE: LOW. Machine response limited.")
        elif level == "MEDIUM":
            print(">>> STATE: MEDIUM. Structured delivery optimal.")
        else:
            print(">>> STATE: HIGH. Full bandwidth available.")
        
        record = {
            "cycle_id": cycle_id,
            "timestamp": datetime.now().isoformat(),
            "score": decision['score'],
            "veto_armed": self.veto_armed,
            "level": level
        }
        
        await self.executor.execute("write_data", {"record": record})
        return record
    
    async def shutdown(self):
        await self.sensor.cleanup()
        # Final Purge on exit
        if os.path.exists("VETO_ACTIVE.lock"):
            os.remove("VETO_ACTIVE.lock")
        print("\nPurge protocol complete. Gate silent.")

async def main():
    veto = BioSignalVeto()
    await veto.initialize()
    
    try:
        cycle = 1
        while True: # Continuous flow
            await veto.run_cycle(cycle)
            await asyncio.sleep(4) # 4 second interval
            cycle += 1
    except KeyboardInterrupt:
        await veto.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
