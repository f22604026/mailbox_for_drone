#!/usr/bin/env python

import wiringpi as wpi
import time

wpi.wiringPiSetup()
wpi.pinMode(5, 1)
wpi.pinMode(23, 1)

while True:
    input = raw_input("Secure the package, enter '1' \nRelease the package, enter '2'  \ndoor opening, enter '3':\n ==> ")
    if input == "1" :
        print("Package is secured! \n")
        wpi.digitalWrite(5, 0)
    if input == "2" :
        print("Package is released! \n")
        wpi.digitalWrite(5, 1)

    if input == "3" :
        print("door opening! \n")
        wpi.digitalWrite(23, 1)
        time.sleep(1000)
        wpi.digitalWrite(23, 0)
