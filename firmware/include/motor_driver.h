#pragma once

#include <Arduino.h>

// Motor Driver Class Skeleton
class MotorDriver {
public:
    MotorDriver(uint8_t pwm_pin, uint8_t dir_pin, uint8_t channel = 0)
        : pwm_pin_(pwm_pin), dir_pin_(dir_pin), channel_(channel) {}

    void init() {
        // TODO: Initialize GPIO pins and PWM channels
    }

    void setEffort(float effort) {
        // TODO: Drive motor with directional PWM effort
    }

    void stop() {
        // TODO: Set PWM effort to zero
    }

private:
    uint8_t pwm_pin_;
    uint8_t dir_pin_;
    uint8_t channel_;
};
