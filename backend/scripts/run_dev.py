#!/usr/bin/env python3
"""
scripts/run_dev.py – Development server launcher.

Usage:
    cd backend
    python scripts/run_dev.py
"""

import subprocess
import sys

if __name__ == "__main__":
    subprocess.run(
        [
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000",
        ],
        check=True,
    )
