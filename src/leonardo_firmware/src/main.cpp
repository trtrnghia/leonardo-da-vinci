/**
 * Production ESP32-S3 Firmware for Leonardo da Vinci Drawing Robot.
 * Implements 3-channel velocity PID control, quadrature encoder interrupts,
 * servo pen actuation, ASCII command parsing, and safety watchdog timer.
 */

#include <Arduino.h>
#include <ESP32Servo.h>
#include "config.h"
#include "pid_controller.h"
#include "motor_driver.h"
#include "encoder_reader.h"
#include "serial_protocol.h"

// Hardware Devices
MotorDriver motor1(MOTOR1_PWM_PIN, MOTOR1_DIR_PIN, 0);
MotorDriver motor2(MOTOR2_PWM_PIN, MOTOR2_DIR_PIN, 1);
MotorDriver motor3(MOTOR3_PWM_PIN, MOTOR3_DIR_PIN, 2);

EncoderReader enc1(ENC1_A_PIN, ENC1_B_PIN);
EncoderReader enc2(ENC2_A_PIN, ENC2_B_PIN);
EncoderReader enc3(ENC3_A_PIN, ENC3_B_PIN);

PIDController pid1(DEFAULT_KP, DEFAULT_KI, DEFAULT_KD);
PIDController pid2(DEFAULT_KP, DEFAULT_KI, DEFAULT_KD);
PIDController pid3(DEFAULT_KP, DEFAULT_KI, DEFAULT_KD);

Servo penServo;
bool penDown = false;

// Speed targets and measurements in rad/s
float target_w1 = 0.0f, target_w2 = 0.0f, target_w3 = 0.0f;
float meas_w1 = 0.0f, meas_w2 = 0.0f, meas_w3 = 0.0f;

// Timers and Watchdog
unsigned long lastControlTime = 0;
unsigned long lastTelemetryTime = 0;
unsigned long lastSerialMsgTime = 0;

// ISR wrappers for encoders
void IRAM_ATTR isr_enc1() { enc1.handleInterrupt(); }
void IRAM_ATTR isr_enc2() { enc2.handleInterrupt(); }
void IRAM_ATTR isr_enc3() { enc3.handleInterrupt(); }

void setPen(bool down) {
    penDown = down;
    if (penDown) {
        penServo.write(PEN_DOWN_ANGLE);
    } else {
        penServo.write(PEN_UP_ANGLE);
    }
}

void setup() {
    Serial.begin(BAUDRATE);

    // Initialize Motor Drivers
    motor1.init();
    motor2.init();
    motor3.init();

    // Initialize Encoders & attach ISRs
    enc1.init();
    enc2.init();
    enc3.init();
    attachInterrupt(digitalPinToInterrupt(ENC1_A_PIN), isr_enc1, CHANGE);
    attachInterrupt(digitalPinToInterrupt(ENC2_A_PIN), isr_enc2, CHANGE);
    attachInterrupt(digitalPinToInterrupt(ENC3_A_PIN), isr_enc3, CHANGE);

    // Initialize Servo
    ESP32PWM::allocateTimer(0);
    penServo.setPeriodHertz(50);
    penServo.attach(SERVO_PIN, 500, 2400);
    setPen(false); // Default Pen UP

    lastControlTime = micros();
    lastTelemetryTime = millis();
    lastSerialMsgTime = millis();

    Serial.println("INFO Leonardo ESP32-S3 Firmware initialized.");
}

void loop() {
    unsigned long nowMillis = millis();

    // 1. Process Serial Commands
    while (Serial.available() > 0) {
        String line = Serial.readStringUntil('\n');
        line.trim();
        if (line.length() == 0) continue;

        lastSerialMsgTime = nowMillis;
        RobotCommand cmd = SerialProtocol::parseLine(line);

        switch (cmd.type) {
            case RobotCommand::PEN_UP:
                setPen(false);
                SerialProtocol::sendAck("P0");
                break;
            case RobotCommand::PEN_DOWN:
                setPen(true);
                SerialProtocol::sendAck("P1");
                break;
            case RobotCommand::MOTOR_SPEEDS:
                target_w1 = cmd.w1;
                target_w2 = cmd.w2;
                target_w3 = cmd.w3;
                break;
            case RobotCommand::STOP:
                target_w1 = target_w2 = target_w3 = 0.0f;
                setPen(false);
                pid1.reset();
                pid2.reset();
                pid3.reset();
                motor1.stop();
                motor2.stop();
                motor3.stop();
                SerialProtocol::sendAck("S");
                break;
            default:
                break;
        }
    }

    // 2. Watchdog Check (500ms safety timeout)
    if (nowMillis - lastSerialMsgTime > WATCHDOG_TIMEOUT_MS) {
        target_w1 = target_w2 = target_w3 = 0.0f;
        setPen(false);
        motor1.stop();
        motor2.stop();
        motor3.stop();
    }

    // 3. High-Frequency Control Loop (100 Hz / dt = 0.01s)
    unsigned long nowMicros = micros();
    float dt = (nowMicros - lastControlTime) * 1e-6f;
    if (dt >= (1.0f / CONTROL_LOOP_FREQ_HZ)) {
        lastControlTime = nowMicros;

        // Measure actual velocities
        meas_w1 = enc1.getVelocityRadPerSec(dt, TOTAL_TICKS_PER_REV);
        meas_w2 = enc2.getVelocityRadPerSec(dt, TOTAL_TICKS_PER_REV);
        meas_w3 = enc3.getVelocityRadPerSec(dt, TOTAL_TICKS_PER_REV);

        // PID update
        float effort1 = pid1.update(target_w1, meas_w1, dt);
        float effort2 = pid2.update(target_w2, meas_w2, dt);
        float effort3 = pid3.update(target_w3, meas_w3, dt);

        // Drive motors
        motor1.setEffort(effort1);
        motor2.setEffort(effort2);
        motor3.setEffort(effort3);
    }

    // 4. Periodic Telemetry Stream (50 Hz / 20ms)
    if (nowMillis - lastTelemetryTime >= (1000 / TELEMETRY_FREQ_HZ)) {
        lastTelemetryTime = nowMillis;
        SerialProtocol::sendTelemetry(penDown, meas_w1, meas_w2, meas_w3);
    }
}
