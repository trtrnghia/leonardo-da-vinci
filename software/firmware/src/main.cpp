/**
 * ESP32-S3 Firmware Skeleton for Leonardo da Vinci Drawing Robot.
 */

#include <Arduino.h>
#include "config.h"
#include "pid_controller.h"
#include "motor_driver.h"
#include "encoder_reader.h"
#include "serial_protocol.h"

void setup() {
    Serial.begin(BAUDRATE);
    // TODO: Initialize peripherals, motors, encoders, and servo
    Serial.println("INFO Leonardo ESP32-S3 Firmware Skeleton ready.");
}

void loop() {
    // TODO: Serial command parsing, closed-loop PID control, and telemetry streaming
    delay(10);
}
