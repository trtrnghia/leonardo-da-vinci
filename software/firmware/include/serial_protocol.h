#pragma once

#include <Arduino.h>

// Serial Protocol Parser and Telemetry Skeleton
struct RobotCommand {
    enum Type { NONE, PEN_UP, PEN_DOWN, MOTOR_SPEEDS, STOP };
    Type type;
    float w1, w2, w3;
};

class SerialProtocol {
public:
    static RobotCommand parseLine(const String& line) {
        // TODO: Parse command string (P0, P1, M, S)
        RobotCommand cmd;
        cmd.type = RobotCommand::NONE;
        return cmd;
    }

    static void sendAck(const char* cmd_name) {
        // TODO: Send ACK response
    }

    static void sendTelemetry(bool pen_down, float w1, float w2, float w3) {
        // TODO: Format and send periodic telemetry stream
    }
};
