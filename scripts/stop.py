"""Stop the known Caudal development supervisor, preserving database services."""

import json
import os
import signal
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
state_path = root / ".local/run.json"
if not state_path.exists():
    raise SystemExit("No CaudalTickets supervisor is registered.")
pid = int(json.loads(state_path.read_text())["supervisor"])
try:
    command = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
except FileNotFoundError:
    state_path.unlink(missing_ok=True)
    raise SystemExit("The recorded supervisor has already stopped.") from None
if os.fsencode(root / "scripts/dev.py") not in command:
    raise SystemExit(
        "The recorded PID is not this checkout's supervisor; no signal was sent."
    )
os.kill(pid, signal.SIGTERM)
for _ in range(250):
    if not state_path.exists():
        print(
            "CaudalTickets web and API stopped; database and mail services preserved."
        )
        break
    time.sleep(0.1)
else:
    raise SystemExit("The supervisor did not finish stopping; inspect .local logs.")
