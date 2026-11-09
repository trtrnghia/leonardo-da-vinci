#pragma once

#include <Arduino.h>

// Communication
#define BAUDRATE 115200
#define SERIAL_TIMEOUT_MS 100
#define WATCHDOG_TIMEOUT_MS 500

// Control Loop Frequencies
#define CONTROL_LOOP_FREQ_HZ 100
#define TELEMETRY_FREQ_HZ 50

// Robot Geometry
#define ROBOT_RADIUS_M 0.15f
#define WHEEL_RADIUS_M 0.029f
#define ENCODER_CPR 334.0f
#define GEAR_RATIO 30.0f
#define TOTAL_TICKS_PER_REV (ENCODER_CPR * GEAR_RATIO)

// Pen Mechanism (Servo)
#define SERVO_PIN 4
#define PEN_UP_ANGLE 30
#define PEN_DOWN_ANGLE 90

// Motor 1 (Wheel 1: 0 deg)
#define MOTOR1_PWM_PIN 5
#define MOTOR1_DIR_PIN 6
#define ENC1_A_PIN 11
#define ENC1_B_PIN 12

// Motor 2 (Wheel 2: 120 deg)
#define MOTOR2_PWM_PIN 7
#define MOTOR2_DIR_PIN 8
#define ENC2_A_PIN 13
#define ENC2_B_PIN 14

// Motor 3 (Wheel 3: 240 deg)
#define MOTOR3_PWM_PIN 9
#define MOTOR3_DIR_PIN 10
#define ENC3_A_PIN 15
#define ENC3_B_PIN 16

// Default PID Gains
#define DEFAULT_KP 2.5f
#define DEFAULT_KI 0.8f
#define DEFAULT_KD 0.05f
