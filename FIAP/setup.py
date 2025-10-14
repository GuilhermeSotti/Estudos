import os, sys, subprocess
from pathlib import Path

def create_venv(venv=".venv", req="Cap 1 - Despertar da rede neural/requirements.txt"):
    venv, req = Path(venv), Path(req)

    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)

    pip = venv / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
    subprocess.run([str(pip), "install", "-r", str(req)], check=True)

if __name__ == "__main__":
    create_venv()
