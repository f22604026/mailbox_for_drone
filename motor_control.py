#!/usr/bin/env python

import wiringpi as wpi
import time

wpi.wiringPiSetup()
wpi.pinMode(5, 1)

while True:
    input = raw_input("Secure the package, enter '1' \nRelease the package, enter '2':\n ==> ")
    if input == "1" :
        print("Package is secured! \n")
        wpi.digitalWrite(5, 0)
    if input == "2" :
        print("Package is released! \n")
        wpi.digitalWrite(5, 1)
