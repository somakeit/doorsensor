#!/usr/bin/env python
import os
import signal
import shlex
import subprocess
import wiringpi2
from time import time, sleep
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Some of these constants are from
# https://github.com/WiringPi/WiringPi/blob/master/wiringPi/wiringPi.h
INPUT = 0
OUTPUT = 1
PWM_OUTPUT = 2
LOW = 0
HIGH = 1
PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2

# Use wiringPi numbering scheme - pin1 is PWM (PCM_CLK)
wiringpi2.wiringPiSetup()

# Switch on wiring pi pin 4 (GPIO 23)
DOOR_PIN = 4
# Switch on wiring pi pin 0 (GPIO 17)
SPACE_PIN = 0

# How many times per second should we read the GPIO?
FREQUENCY = 2

# Global variables
detected = 0
notified = 0
spaceIsOpen = False

wiringpi2.pinMode(DOOR_PIN, INPUT)
wiringpi2.pullUpDnControl(DOOR_PIN, PUD_UP)
wiringpi2.pinMode(SPACE_PIN, INPUT)
wiringpi2.pullUpDnControl(SPACE_PIN, PUD_UP)

def say(msg):
    msg = "beep "+msg
    command = "echo {} | festival --tts".format(shlex.quote(msg))
    cmd = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    cmd.wait()

while True:
    if not wiringpi2.digitalRead(DOOR_PIN):
        detected = time()
        if time() - notified > 30:
            notified = time()
            print("DOOR IS OPEN")
            if spaceIsOpen:
                say("the door is open")
    else:
        # Reset
        notified = 0

    if not wiringpi2.digitalRead(SPACE_PIN):
        if not spaceIsOpen:
            spaceIsOpen = True
            say("the space is open")
    else:
        if spaceIsOpen:
            spaceIsOpen = False
            say("the space is closed")

    sleep(1.0/FREQUENCY)
