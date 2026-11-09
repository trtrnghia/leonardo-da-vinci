#pragma once

class PIDController {
public:
    PIDController(float kp = 2.0f, float ki = 0.5f, float kd = 0.05f, float out_min = -255.0f, float out_max = 255.0f)
        : kp_(kp), ki_(ki), kd_(kd), min_(out_min), max_(out_max),
          integral_(0.0f), prev_error_(0.0f) {}

    void setGains(float kp, float ki, float kd) {
        kp_ = kp;
        ki_ = ki;
        kd_ = kd;
    }

    void reset() {
        integral_ = 0.0f;
        prev_error_ = 0.0f;
    }

    float update(float target, float current, float dt) {
        if (dt <= 0.0f) return 0.0f;

        float error = target - current;

        // Proportional
        float p_term = kp_ * error;

        // Integral with anti-windup clamping
        integral_ += error * dt;
        float i_term = ki_ * integral_;

        // Derivative
        float d_term = kd_ * (error - prev_error_) / dt;
        prev_error_ = error;

        float output = p_term + i_term + d_term;

        // Output clamping
        if (output > max_) {
            output = max_;
            // Clamp integral accumulation
            integral_ -= error * dt;
        } else if (output < min_) {
            output = min_;
            integral_ -= error * dt;
        }

        return output;
    }

private:
    float kp_, ki_, kd_;
    float min_, max_;
    float integral_;
    float prev_error_;
};
