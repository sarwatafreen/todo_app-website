#!/usr/bin/env python3
"""
Development server runner for Todo Full-Stack Web Application
"""

import subprocess
import sys
import os
from pathlib import Path

def run_backend():
    """Run the backend development server."""
    print("Starting backend server...")
    backend_dir = Path("backend")

    if not backend_dir.exists():
        print("Error: backend directory not found")
        return False

    os.chdir(backend_dir)

    try:
        # Run uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
        return True
    except Exception as e:
        print(f"Error starting backend: {e}")
        return False

def main():
    print("Todo Full-Stack Web Application - Development Server")
    print("=" * 50)
    print("Starting backend server on port 8000...")
    print("Press Ctrl+C to stop the server\n")

    run_backend()

if __name__ == "__main__":
    main()