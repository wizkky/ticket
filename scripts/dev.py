"""Supervise local development processes and stop only the groups we started."""

import json
import os
import signal
import socket
import subprocess
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local"
stopping = False


def stop(_signum: int, _frame: object) -> None:
    global stopping
    stopping = True


for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, stop)

for port in (8000, 5173):
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", port)) == 0:
            raise SystemExit(
                f"Port {port} is already in use; stop the existing process before starting another demo."
            )

children = []
logs = []
exit_code = 0
try:
    for name, directory, command in (
        (
            "api",
            "apps/api",
            [
                str(ROOT / "apps/api/.venv/bin/python"),
                "src/manage.py",
                "runserver",
                "127.0.0.1:8000",
                "--noreload",
            ],
        ),
        ("web", "apps/web", ["node", "--env-file=.env", "build"]),
    ):
        log = (LOCAL / f"{name}.log").open("a")
        logs.append(log)
        environment = os.environ.copy()
        if name == "web":
            environment.update(
                HOST="127.0.0.1", PORT="5173", ORIGIN="http://localhost:5173"
            )
        process = subprocess.Popen(
            command,
            cwd=ROOT / directory,
            env=environment,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        children.append(process)
    (LOCAL / "run.json").write_text(
        json.dumps({"supervisor": os.getpid(), "children": [p.pid for p in children]})
    )
    endpoints = ["http://127.0.0.1:8000/api/healthcheck", "http://127.0.0.1:5173/"]
    deadline = time.monotonic() + 120
    while endpoints and not stopping:
        if any(p.poll() is not None for p in children):
            raise RuntimeError(
                "A service stopped during startup; inspect .local/api.log and .local/web.log."
            )
        if time.monotonic() > deadline:
            raise RuntimeError(
                "Services did not become ready within 120 seconds; inspect .local logs."
            )
        for endpoint in endpoints[:]:
            try:
                with urlopen(endpoint, timeout=2) as response:
                    if response.status == 200:
                        endpoints.remove(endpoint)
            except (URLError, TimeoutError):
                pass
        time.sleep(1)
    if not stopping:
        print(
            "CaudalTickets ready: web port 5173, API port 8000, local mail port 8025. Logs: .local/. Stop with bash scripts/stop.sh.",
            flush=True,
        )
    while not stopping:
        if any(p.poll() is not None for p in children):
            raise RuntimeError("A development service stopped; inspect .local logs.")
        time.sleep(1)
except RuntimeError as error:
    print(error, flush=True)
    exit_code = 1
finally:
    for process in children:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
    for process in children:
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
    for log in logs:
        log.close()
    (LOCAL / "run.json").unlink(missing_ok=True)
raise SystemExit(exit_code)
