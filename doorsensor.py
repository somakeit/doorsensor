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
firstLoop = True
still = ""

wiringpi2.pinMode(DOOR_PIN, INPUT)
wiringpi2.pullUpDnControl(DOOR_PIN, PUD_UP)
wiringpi2.pinMode(SPACE_PIN, INPUT)
wiringpi2.pullUpDnControl(SPACE_PIN, PUD_UP)

def say(msg):
    command = "echo {} | festival --tts".format(shlex.quote(msg))
    cmd = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    cmd.wait()

def smib(msg):
    command = "echo {} | nc localhost 1337".format(shlex.quote(msg))
    cmd = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    cmd.wait()

smib("Door sensor script started.")
while True:
    if not wiringpi2.digitalRead(DOOR_PIN):
        detected = time()
        if time() - notified > 30:
            notified = time()
            print("DOOR IS OPEN")
            if spaceIsOpen:
                say("the door is " + still + "open")
                still = "still "
    else:
        # Reset
        notified = 0
        still = ""

    if not wiringpi2.digitalRead(SPACE_PIN):
        if not spaceIsOpen:
            spaceIsOpen = True
            if not firstLoop:
                smib("The space is now open - come join us!")
                say("The space is open, unlock the fire escape.")
    else:
        if spaceIsOpen:
            spaceIsOpen = False
            if not firstLoop:
                smib("The space is now closed - see you next time!")
                say("the space is closed")

    firstLoop = False
    sleep(1.0/FREQUENCY)
