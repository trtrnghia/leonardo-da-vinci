#pragma once

#include <Arduino.h>

class EncoderReader {
public:
    EncoderReader(uint8_t pin_a, uint8_t pin_b)
        : pin_a_(pin_a), pin_b_(pin_b), count_(0), prev_count_(0) {}

    void init() {
        pinMode(pin_a_, INPUT_PULLUP);
        pinMode(pin_b_, INPUT_PULLUP);
    }

    void IRAM_ATTR handleInterrupt() {
        if (digitalRead(pin_a_) == digitalRead(pin_b_)) {
            count_++;
        } else {
            count_--;
        }
    }

    int32_t getCount() const {
        return count_;
    }

    float getVelocityRadPerSec(float dt, float ticks_per_rev) {
        if (dt <= 0.0f) return 0.0f;
        int32_t delta_ticks = count_ - prev_count_;
        prev_count_ = count_;
        float revs = (float)delta_ticks / ticks_per_rev;
        return (revs * 2.0f * PI) / dt;
    }

private:
    uint8_t pin_a_;
    uint8_t pin_b_;
    volatile int32_t count_;
    int32_t prev_count_;
};
