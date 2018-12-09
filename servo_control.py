#!/usr/bin/env python
# Hung-Chen Yu 11-10-2018 test

import numpy as np
import math
import mavros_msgs
import time
import sys
import wiringpi


def main():
    # use 'GPIO naming'
    servo_pin =
    wiringpi.wiringPiSetupGpio()

    # set #18 to be a PWM output
    wiringpi.pinMode(servo_pin, wiringpi.GPIO.PWM_OUTPUT)

    # set the PWM mode to milliseconds stype
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

    # divide down clock
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)

    delay_period = 0.01

    while True:
            for pulse in range(50, 250, 1):
                    wiringpi.pwmWrite(servo_pin, pulse)
                    time.sleep(delay_period)
            for pulse in range(250, 50, -1):
                    wiringpi.pwmWrite(servo_pin, pulse)
                    time.sleep(delay_period)


if __name__ == '__main__':
    main()
