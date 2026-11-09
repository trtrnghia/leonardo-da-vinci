#pragma once

#include <Arduino.h>

// Quadrature Encoder Reader Class Skeleton
class EncoderReader {
public:
    EncoderReader(uint8_t pin_a, uint8_t pin_b)
        : pin_a_(pin_a), pin_b_(pin_b), count_(0) {}

    void init() {
        // TODO: Configure pins and attach interrupts
    }

    void handleInterrupt() {
        // TODO: Decode quadrature state
    }

    int32_t getCount() const {
        return count_;
    }

    float getVelocityRadPerSec(float dt, float ticks_per_rev) {
        // TODO: Compute angular velocity
        return 0.0f;
    }

private:
    uint8_t pin_a_;
    uint8_t pin_b_;
    volatile int32_t count_;
};
