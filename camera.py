#!/usr/bin/env python
# this file is run using this command: "sudo python camera.py"
# python must be installed, and you must call the command while
# you are in the same folder as the file
from time import sleep
import os
import RPi.GPIO as GPIO
import subprocess
import datetime
import pygame
pygame.init()

# set up the pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(18,GPIO.IN)
# setup variables
count = 0
up = False
down = False
command = ""
command_shut = ""
filename = ""
index = 0
camera_pause = "500"
print "Raspberry Pi Camera with Buttons"
def takepic(imageName):
        print("click")
        command = "sudo raspistill -o " + imageName + " -q 100 -t " + camera_pause
        print(command)
        os.system(command)
while(True):
        GPIO.output(23,True)
        # for event in pygame.event.get():
        #       if event.type == pygame.QUIT: sys.exit()
        if(up==True):
                if(GPIO.input(24)==False):
                        print "BUTTON DOWN PRESSED"
                        now = datetime.datetime.now()
                        timeString = now.strftime("%Y-%m-%d_%H:%M:%S")
                        print("request received" + timeString)
                        filename = "photos/photo-" + timeString + ".jpg"
                        takepic(filename)
                        # On envoie sur la Dropbox
                        from subprocess import call  
                        photofile = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/" + filename + " " + filename
                        call ([photofile], shell=True)
                if(GPIO.input(18)==False):
                        command_shut = "sudo halt"
                        print(command_shut)
                        # os.system(command_shut)
        up = GPIO.input(24)
        count = count +1
        sleep(.1)
# this is never hit, but should be here to indicate if you plan on leaving the main loop
print "done"