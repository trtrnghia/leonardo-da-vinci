#pragma once

#include <Arduino.h>

class MotorDriver {
public:
    MotorDriver(uint8_t pwm_pin, uint8_t dir_pin, uint8_t pwm_channel = 0)
        : pwm_pin_(pwm_pin), dir_pin_(dir_pin), pwm_channel_(pwm_channel) {}

    void init() {
        pinMode(dir_pin_, OUTPUT);
        pinMode(pwm_pin_, OUTPUT);
        // Using standard Arduino analogWrite or ledc
        analogWrite(pwm_pin_, 0);
        digitalWrite(dir_pin_, LOW);
    }

    void setEffort(float effort) {
        // effort in range [-255, 255]
        if (effort > 0.0f) {
            digitalWrite(dir_pin_, HIGH);
            int pwm_val = constrain((int)effort, 0, 255);
            analogWrite(pwm_pin_, pwm_val);
        } else if (effort < 0.0f) {
            digitalWrite(dir_pin_, LOW);
            int pwm_val = constrain((int)(-effort), 0, 255);
            analogWrite(pwm_pin_, pwm_val);
        } else {
            analogWrite(pwm_pin_, 0);
        }
    }

    void stop() {
        analogWrite(pwm_pin_, 0);
    }

private:
    uint8_t pwm_pin_;
    uint8_t dir_pin_;
    uint8_t pwm_channel_;
};
