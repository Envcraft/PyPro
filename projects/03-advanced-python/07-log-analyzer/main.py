#!/usr/bin/env python3
"""Main application entry point for Log Analyzer."""

import sys
from pathlib import Path

# Add src directory to sys.path so package imports resolve cleanly
src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from log_analyzer.cli import main

if __name__ == "__main__":
    sys.exit(main())
