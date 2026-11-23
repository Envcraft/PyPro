"""Test suite package initialization."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"

for path_str in (str(project_root), str(src_dir)):
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
