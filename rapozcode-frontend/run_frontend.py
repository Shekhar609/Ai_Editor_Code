#!/usr/bin/env python3
"""
RapoZCode Frontend Startup Script
This script starts the Streamlit frontend application.
"""

import subprocess
import sys
import os

def main():
    """Start the Streamlit frontend application"""
    print("🚀 Starting RapoZCode Frontend...")
    print("📱 Frontend will be available at: http://localhost:8501")
    print("🔗 Backend should be running at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped.")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 