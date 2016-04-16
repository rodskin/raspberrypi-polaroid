#!/usr/bin/env python
# this file is run using this command: "sudo python camera.py"
# python must be installed, and you must call the command while
# you are in the same folder as the file
from time import sleep
import os
import RPi.GPIO as GPIO
import subprocess
import Image
import datetime
import pygame
import urllib2
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
dir_name = "photos"
filename = ""
index = 0
camera_pause = "500"
photoResize = 512, 384
print "Raspberry Pi Camera with Buttons"
def takepic(imageName):
    print("click")
    #command = "sudo raspistill -o " + imageName + " -q 100 -t " + camera_pause
    command = "sudo raspistill -p '144,48,512,384' --vflip -w 1920 -h 1440 -o " + imageName
    # print(command)
    os.system(command)
#internet detection
def internet_on():
    try:
        response=urllib2.urlopen('http://google.com',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False
while(True):
    GPIO.output(23,True)
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT: sys.exit()
    if(up==True):
        if(GPIO.input(24)==False):
            print "BUTTON CAMERA PRESSED"
            now = datetime.datetime.now()
            timeString = now.strftime("%Y-%m-%d_%H:%M:%S")
            print("request received" + timeString)
            filename = "photo-" + timeString + ".jpg"
            takepic(dir_name + "/" + filename)
            Image.open(dir_name + "/" + filename).resize(photoResize, Image.ANTIALIAS).save(dir_name + "/" + "thumbnail.jpg")
            Image.open(photoPath + "thumbnail.jpg").transpose(2).save(photoPath + "thumbnail-rotated.jpg")
            # Print the PHoto
            printer.begin(90) # Warmup time
            printer.setTimes(40000, 3000) # Set print and feed times
            printer.justify('C') # Center alignment
            printer.printImage(Image.open(photoPath + "line-top.png"), True)
            printer.println(photoTitle)
            printer.printImage(Image.open(photoPath + "line-bottom.png"), True)
            printer.feed(1) # Add a blank line
            printer.printImage(Image.open(photoPath + "thumbnail-rotated.jpg"), True) # Specify image to print
            printer.feed(1) # Add a blank line
            printer.printImage(Image.open(photoPath + "qr-code.png"), True) # Specify image to print
            printer.feed(3) # Add a few blank lines
            # On envoie sur la Dropbox
            #from subprocess import call  
            #photofile = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload " + dir_name + "/" + filename + " " + filename
            #call ([photofile], shell=True)
        #if(GPIO.input(18)==False):
        #    GPIO.output(23,False)
        #    command_shut = "sudo halt"
        #    print(command_shut)
            # os.system(command_shut)
    up = GPIO.input(24)
    count = count +1
    sleep(.1)
# this is never hit, but should be here to indicate if you plan on leaving the main loop
print "done"