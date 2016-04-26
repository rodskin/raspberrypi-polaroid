#!/usr/bin/env python
# this file is run using this command: "sudo python camera.py"
# python must be installed, and you must call the command while
# you are in the same folder as the file
from time import sleep
#from __future__ import print_function
import os
import RPi.GPIO as GPIO
import subprocess
import Image
import datetime
import time
import pygame
import urllib2
import sys
#sys.path.append("/home/pi/Python-Thermal-Printer")
#from Adafruit_Thermal import *
pygame.init()

# Define printer
#printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)


# set up the pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT) #LED lorsque le programme est charge
GPIO.setup(24,GPIO.IN) #bouton de prise de photo en passe bas
GPIO.setup(18,GPIO.IN) #Eventuel bouton pour eteindre le pi
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
#print "Raspberry Pi Camera with Buttons"
sys.stdout.write('Raspberry Pi Camera with Buttons.')
def takepic(imageName):
    sys.stdout.write("click")
    dir_name = "photos"
    #command = "sudo raspistill -o " + imageName + " -q 100 -t " + camera_pause
    command = "sudo raspistill -p '144,48,512,384' --vflip -w 1920 -h 1440 -o " + imageName
    # print(command)
    os.system(command)
    Image.open(imageName).resize(photoResize, Image.ANTIALIAS).save(dir_name + "/" + "thumbnail.jpg")
    Image.open(dir_name + "/" + "thumbnail.jpg").transpose(2).save(dir_name + "/" + "thumbnail-rotated.jpg")
#internet detection
def internet_on():
    try:
        response=urllib2.urlopen('http://google.com',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def printPicture():
    # Print the Photo
    printer.begin(90) # Warmup time
    printer.setTimes(40000, 3000) # Set print and feed times
    printer.justify('C') # Center alignment
    printer.printImage(Image.open(dir_name + "/" + "line-top.png"), True)
    printer.println(photoTitle)
    printer.printImage(Image.open(dir_name + "/" + "line-bottom.png"), True)
    printer.feed(1) # Add a blank line
    printer.printImage(Image.open(dir_name + "/" + "thumbnail-rotated.jpg"), True) # Specify image to print
    printer.feed(1) # Add a blank line
    #printer.printImage(Image.open(photoPath + "qr-code.png"), True) # Specify image to print
    printer.feed(3) # Add a few blank lines
try:
    while(True):
        GPIO.output(23,True)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT: sys.exit()
        if(up==True):
            if(GPIO.input(24)==False):
                sys.stdout.write("BUTTON CAMERA PRESSED")
                now = datetime.datetime.now()
                timeString = now.strftime("%Y-%m-%d_%H:%M:%S")
                sys.stdout.write("request received" + timeString)
                filename = "photo-" + timeString + ".jpg"
                takepic(dir_name + "/" + filename)
                
                #printPicture()
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
    sys.stdout.write("done")

except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "\n", 'CTRL+C' # print value of counter  
  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print "Other error or exception occurred!"
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  