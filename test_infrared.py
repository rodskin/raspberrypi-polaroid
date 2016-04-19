# this file is run using this command: "sudo python camera.py"
# python must be installed, and you must call the command while
# you are in the same folder as the file
#from time import sleep
from time import sleep
import os
import RPi.GPIO as GPIO
import subprocess
import Image
import datetime
import time
import pygame
import urllib2
import sys

pygame.init()

# set up the pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.IN)
GPIO.setup(25,GPIO.OUT)

infrared = False

while(True):
   infrared = not infrared
   GPIO.output(25,infrared)
   if(GPIO.input(24)==True):
      GPIO.output(25,True)
   else:
      GPIO.output(25,False)

   sleep(.5)