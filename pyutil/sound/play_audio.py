#! /usr/bin/env python
import RPi.GPIO as GPIO # type: ignore
import pygame, time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, True)
time.sleep(1)

import serial.tools.list_ports # type: ignore
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
print (myports)

# pygame.mixer.init()
# pygame.mixer.music.load("short.wav")
# pygame.mixer.music.play()
# while pygame.mixer.music.get_busy():
#     continue
# time.sleep(1)
# GPIO.output(26, False)