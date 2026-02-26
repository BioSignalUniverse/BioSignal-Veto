import os
import json
import asyncio
from pathlib import Path
from enum import Enum


class ActionType(str, Enum):
    VETO_ARM = "veto_arm"
    VETO_RELEASE = "veto_release"
    WRITE_DATA = "write_data"
    WAIT = "wait"


class ActionExecutor:
    def __init__(self, runtime_dir="runtime"):
        self.runtime_path = Path(runtime_dir)
        self.runtime_path.mkdir(exist_ok=True)

        self.lock_file = self.runtime_path / "VETO_ACTIVE.lock"
        self.log_file = self.runtime_path / "session_log.jsonl"

    async def execute(self, action_type: ActionType, data=None):
        data = data or {}

        if action_type == ActionType.VETO_ARM:
            self.lock_file.write_text("LOCKED")
            print(f"!!! VETO ARMED: {self.lock_file} created !!!")

        elif action_type == ActionType.VETO_RELEASE:
            if self.lock_file.exists():
                self.lock_file.unlink()
            print("--- VETO RELEASED: Lock file removed ---")

        elif action_type == ActionType.WRITE_DATA:
            with self.log_file.open("a") as f:
                f.write(json.dumps(data) + "\n")

        elif action_type == ActionType.WAIT:
            await asyncio.sleep(data.get("duration", 1))