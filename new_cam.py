#!/usr/bin/env python
from __future__ import print_function
import os
import time
import Image
import sys
sys.path.append("/home/pi/Python-Thermal-Printer")
from Adafruit_Thermal import *

# Some variables
photoPath = "/home/pi/photobooth/"
photoName = time.strftime("%Y%m%d%H%M%S") + "_photobooth.jpg"
photoResize = 512, 384
#photoTitle = "Rod's polaroid"
photoTitle = time.strftime("%d%m%Y %H%M")

# Define printer
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

# Callback function for photo button
def photo_callback(obj):
        # Define filename with timestamp
        photoName = time.strftime("%Y%m%d%H%M%S") + "_photobooth.jpg"
        # Take photo using "raspistill"
        os.system("sudo raspistill -p '144,48,512,384' --vflip -w 1920 -h 1440 -o " + photoPath + photoName)
        # Resize the high res photo to create thumbnail
        Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "thumbnail.jpg")

# Callback function for print button
def print_callback(obj):
        # Rotate the thumbnail for printing
        Image.open(photoPath + "thumbnail.jpg").transpose(2).save(photoPath + "thumbnail-rotated.jpg")
        # Print the foto
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


class MyApp(App):
        # Display the latest thumbnail
        photo = kivyImage(source="/home/pi/photobooth/thumbnail.jpg")

        def build(self):
                # Set up the layout
                photobox = GridLayout(cols=3, spacing=10, padding=10)

                # Create the UI objects (and bind them to callbacks, if necessary)
                photoButton = Button(text="photo", size_hint=(.20, 1)) # Button: 20% width, 100% height
                photoButton.bind(on_press=photo_callback) # when pressed, trigger the photo_callback function
                printButton = Button(text="print", size_hint=(.20, 1)) # Button: 20% width, 100% height
                printButton.bind(on_press=print_callback) # when pressed, trigger the print_callback function

                # Periodically refresh the displayed photo using the callback function
                Clock.schedule_interval(self.callback, 1)

                # Add the UI elements to the layout
                photobox.add_widget(photoButton)
                photobox.add_widget(self.photo)
                photobox.add_widget(printButton)

                return photobox
                
                
        # Callback for thumbnail refresh
        def callback(self, instance):
                self.photo.reload()


if __name__ == '__main__':
        MyApp().run()