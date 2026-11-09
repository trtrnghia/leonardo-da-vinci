/**
 * ESP32-S3 Firmware Skeleton for Leonardo da Vinci Robot
 * Protocol:
 *  - Commands from Pi: P0 (Pen UP), P1 (Pen DOWN), M w1 w2 w3 (Set speeds), S (Stop)
 *  - Responses to Pi: ACK <cmd>, STATUS <pen> <w1> <w2> <w3>
 */

#include <Arduino.h>
#include "config.h"

void setup() {
    Serial.begin(BAUDRATE);
    // Skeleton setup - hardware peripheral initialization
}

void loop() {
    // Skeleton loop - serial command parsing and closed-loop motor control
    if (Serial.available() > 0) {
        String cmd = Serial.readStringUntil('\n');
        cmd.trim();
        if (cmd == "P0") {
            Serial.println("ACK P0");
        } else if (cmd == "P1") {
            Serial.println("ACK P1");
        } else if (cmd == "S") {
            Serial.println("ACK S");
        }
    }
    delay(10);
}
