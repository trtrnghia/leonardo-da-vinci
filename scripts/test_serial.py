#!/usr/bin/env python3
"""Wrapper script to execute software/scripts/test_serial.py."""

import runpy
from pathlib import Path


def main() -> None:
    """Execute target diagnostic script."""
    root = Path(__file__).resolve().parent.parent
    target = root / "software" / "scripts" / "test_serial.py"
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
