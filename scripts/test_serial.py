#!/usr/bin/env python3
"""
Hardware diagnostic script for ESP32-S3 Serial Communication.
Tests connection, command execution (P0, P1, M, S), and prints incoming telemetry.
Usage: python3 scripts/test_serial.py [/dev/ttyACM0]
"""

import sys
import time

try:
    import serial
except ImportError:
    print("Error: pyserial is not installed. Install via: pip install pyserial")
    sys.exit(1)


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    baud = 115200

    print(f"Connecting to ESP32-S3 on {port} @ {baud}...")
    try:
        ser = serial.Serial(port, baud, timeout=1.0)
        time.sleep(2.0)  # Wait for ESP32 reboot upon DTR toggle
    except Exception as e:
        print(f"Failed to open port {port}: {e}")
        return

    print("Connected! Sending Pen UP command: 'P0\\n'")
    ser.write(b"P0\n")
    print(f"Response: {ser.readline().decode('ascii', errors='ignore').strip()}")

    time.sleep(1.0)
    print("Sending Pen DOWN command: 'P1\\n'")
    ser.write(b"P1\n")
    print(f"Response: {ser.readline().decode('ascii', errors='ignore').strip()}")

    time.sleep(1.0)
    print("Sending Motor Speeds: 'M 1.57 -1.57 0.00\\n'")
    ser.write(b"M 1.57 -1.57 0.00\n")

    print("Listening to telemetry for 3 seconds...")
    start_t = time.time()
    while time.time() - start_t < 3.0:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if line:
            print(f"  [ESP32] {line}")

    print("Sending Emergency Stop command: 'S\\n'")
    ser.write(b"S\n")
    print(f"Response: {ser.readline().decode('ascii', errors='ignore').strip()}")

    ser.close()
    print("Serial diagnostics completed successfully.")


if __name__ == "__main__":
    main()
