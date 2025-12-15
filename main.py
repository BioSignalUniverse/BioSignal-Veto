import asyncio
import json
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
        print("BIOSIGNAL VETO GATE v1.0 — PURGE PROTOCOL ENGAGED")
        print("="*60)
        connected = await self.sensor.discover_and_connect()
        print("REAL SENSOR ACTIVE" if connected else "SIMULATION MODE")
    
    async def run_cycle(self, cycle_id: int):
        print(f"\nCycle {cycle_id} — Measuring biosignals")
        raw = await self.sensor.measure()
        
        if raw["signal_quality"] < 0.7:
            print("Signal quality low — cycle discarded")
            return
        
        features = self.processor.calculate_features(raw)
        decision = self.gate.evaluate(features, raw)
        
        print(f"Score: {decision['score']:.3f} → {decision['decision']}")
        print(f"Veto: {decision['veto_status']}")
        
        # Veto arm logic
        if decision["veto_eligible"]:
            self.consecutive += 1
            if self.consecutive >= 2 and not self.veto_armed:
                await self.executor.execute("veto_arm")
                self.veto_armed = True
        else:
            self.consecutive = 0
            if self.veto_armed:
                await self.executor.execute("veto_release")
                self.veto_armed = False
        
        record = {
            "cycle_id": cycle_id,
            "timestamp": datetime.now().isoformat(),
            "raw": raw,
            "features": features,
            "decision": decision,
            "veto_armed": self.veto_armed
        }
        
        await self.executor.execute("write_data", {"record": record})
        
        if decision["decision"] == "WAIT":
            await self.executor.execute("wait", {"duration": 3})
    
    async def shutdown(self):
        await self.sensor.cleanup()
        print("\nPurge protocol complete. Gate silent.")

async def main():
    veto = BioSignalVeto()
    await veto.initialize()
    
    cycles = 10
    interval = 4
    
    for i in range(1, cycles + 1):
        await veto.run_cycle(i)
        if i < cycles:
            await asyncio.sleep(interval)
    
    await veto.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
