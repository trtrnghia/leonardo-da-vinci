#pragma once

#include <Arduino.h>

struct RobotCommand {
    enum Type { NONE, PEN_UP, PEN_DOWN, MOTOR_SPEEDS, STOP };
    Type type;
    float w1, w2, w3;
};

class SerialProtocol {
public:
    static RobotCommand parseLine(const String& line) {
        RobotCommand cmd;
        cmd.type = RobotCommand::NONE;
        cmd.w1 = cmd.w2 = cmd.w3 = 0.0f;

        if (line.startsWith("P0")) {
            cmd.type = RobotCommand::PEN_UP;
        } else if (line.startsWith("P1")) {
            cmd.type = RobotCommand::PEN_DOWN;
        } else if (line.startsWith("S")) {
            cmd.type = RobotCommand::STOP;
        } else if (line.startsWith("M ")) {
            cmd.type = RobotCommand::MOTOR_SPEEDS;
            // Parse: M <w1> <w2> <w3>
            char buf[64];
            line.toCharArray(buf, sizeof(buf));
            sscanf(buf, "M %f %f %f", &cmd.w1, &cmd.w2, &cmd.w3);
        }

        return cmd;
    }

    static void sendAck(const char* cmd_name) {
        Serial.print("ACK ");
        Serial.println(cmd_name);
    }

    static void sendTelemetry(bool pen_down, float w1, float w2, float w3) {
        Serial.print("STATUS ");
        Serial.print(pen_down ? 1 : 0);
        Serial.print(" ");
        Serial.print(w1, 3);
        Serial.print(" ");
        Serial.print(w2, 3);
        Serial.print(" ");
        Serial.println(w3, 3);
    }
};
