import asyncio
import json
import os
from typing import Dict, Any
from datetime import datetime

class ActionExecutor:
    @staticmethod
    async def execute(action: str, params: Dict = None):
        actions = {
            "log": ActionExecutor._log,
            "write_data": ActionExecutor._write_data,
            "wait": ActionExecutor._wait,
            "veto_arm": ActionExecutor._veto_arm,
            "veto_release": ActionExecutor._veto_release
        }
        if action in actions:
            await actions[action](params or {})
    
    @staticmethod
    async def _log(params): 
        print(f"[LOG] {params.get('message', '')}")
    
    @staticmethod
    async def _write_data(params):
        filename = params.get("filename", "data/cycles.json")
        record = params.get("record")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        data = []
        if os.path.exists(filename):
            try:
                with open(filename) as f:
                    data = json.load(f)
            except:
                data = []
        data.append(record)
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    async def _wait(params):
        await asyncio.sleep(params.get("duration", 2))
    
    @staticmethod
    async def _veto_arm(params):
        print("⚡ VETO GATE ARMED — Sovereign coherence confirmed")
    
    @staticmethod
    async def _veto_release(params):
        print("🔓 VETO GATE RELEASED — Coherence lost")
