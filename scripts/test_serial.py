#!/usr/bin/env python3
"""Serial Communication Diagnostic Tool for Leonardo ESP32-S3."""

import sys


def main():
    """Run interactive serial port check."""
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    print(f"Serial diagnostic tool for Leonardo Robot port: {port}")


if __name__ == "__main__":
    main()
