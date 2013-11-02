#!/usr/bin/env python
import os
import signal
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
PIN = 4

# How many times per second should we read the GPIO?
FREQUENCY = 2

# Global variables
detected = 0
notified = 0

wiringpi2.pinMode(PIN, INPUT)
wiringpi2.pullUpDnControl(PIN, PUD_UP)

while True:
  if !wiringpi2.digitalRead(PIN):
    detected = time()
    if time() - notified > 30:
      notified = time()
      print("DOOR IS OPEN")
      command = "echo 'beep the door is open' | festival --tts"
      cmd = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
      cmd.wait()
  else:
    # Reset
    notified = 0

  sleep(1.0/FREQUENCY)
