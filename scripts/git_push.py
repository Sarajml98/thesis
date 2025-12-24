"""Helper script to initialize git, commit, add remote, and push to GitHub.

This script runs git commands via subprocess and prints output. If credentials
are required, git will prompt in the terminal.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTE = "https://github.com/Sarajml98/thesis"

def run(cmd, cwd=ROOT):
    print(f">>> Running: {' '.join(cmd)} (cwd={cwd})")
    proc = subprocess.run(cmd, cwd=str(cwd))
    print(f"Return code: {proc.returncode}\n")
    return proc.returncode

if __name__ == '__main__':
    # Init (if not already a git repo)
    run(["git", "init"])    
    # Add files, commit
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Initial import: thesis project"])    
    # Ensure main branch
    run(["git", "branch", "-M", "main"])    
    # Reset/add remote
    run(["git", "remote", "remove", "origin"])    
    run(["git", "remote", "add", "origin", REMOTE])
    # Push (this will prompt for credentials if required)
    run(["git", "push", "-u", "origin", "main"])    
    print("Done. If push failed due to authentication, follow the prompt or configure credentials (PAT or SSH).")