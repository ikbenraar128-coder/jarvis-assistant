"""
JARVIS - Personal AI Desktop Assistant
Main entry point
"""
import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.interface import main


if __name__ == "__main__":
    try:
        print("="*50)
        print("Starting JARVIS - Personal AI Assistant")
        print("="*50)
        main()
    except KeyboardInterrupt:
        print("\nJARVIS shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
