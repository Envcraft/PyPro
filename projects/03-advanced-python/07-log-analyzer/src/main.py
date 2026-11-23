#!/usr/bin/env python3
"""Log Analyzer — application entry point."""

import sys
from pathlib import Path

# Ensure src directory is in sys.path
src_path = Path(__file__).resolve().parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from log_analyzer.cli import main

if __name__ == "__main__":
    sys.exit(main())
