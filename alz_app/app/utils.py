"""Utility helpers for orchestration and I/O."""
from pathlib import Path
import subprocess
import json
import shlex


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, obj):
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def run_command(command, cwd=None, timeout=None):
    """Run a system command and return (returncode, stdout, stderr).

    command may be list or string. We capture stdout/stderr for logging.
    """
    if isinstance(command, str):
        command = shlex.split(command)
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        return -1, "", f"Timeout: {e}"
    except FileNotFoundError as e:
        return -1, "", str(e)
