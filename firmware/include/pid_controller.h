#pragma once

// PID Controller Class Skeleton
class PIDController {
public:
    PIDController(float kp = 2.0f, float ki = 0.5f, float kd = 0.05f)
        : kp_(kp), ki_(ki), kd_(kd) {}

    void setGains(float kp, float ki, float kd) {
        // TODO: Update PID gains
    }

    void reset() {
        // TODO: Reset integral and derivative state
    }

    float update(float target, float current, float dt) {
        // TODO: Compute PID output
        return 0.0f;
    }

private:
    float kp_, ki_, kd_;
};
