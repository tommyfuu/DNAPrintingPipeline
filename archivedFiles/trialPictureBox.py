"""
Author      : Tom Fu
Date        : 2020 April 8
Description : imageToPrimerPairs.py for DNA Printing Project
"""
# imports for DNAPrinting
import numpy as np
import PIL.ImageStat
import PIL.Image
import math
import os
import imageToGel, distanceToPrimerPairLinear

# imports for GUI
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button

# global variables
imagePath = ""
LENGTH = 36
LANENUM = 20

def primerPairInfoList(image1):
    
    # intialise things
    outputArray = [[False] * LANENUM] * (LENGTH-1) 
    im = PIL.Image.open(image1)
    imgwidth, imgheight = im.size
    boxHeight = imgheight//(LENGTH-1)
    boxWidth = imgwidth//LANENUM
    standard = imageToGel.standardBrightness(im)
    numOfFalses = 0
    total = LANENUM*(LENGTH-1)

    primerPairInfoList = [""]*LANENUM

    # update numOfFalses
    for y in range(0, (LENGTH-1)):
        for x in range(0, LANENUM):
            outputArray[y][x] = imageToGel.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
            if outputArray[y][x] == False:
                numOfFalses += 1
    
    numOfTrues = total - numOfFalses
    print(numOfFalses)
    print(numOfTrues)

    # array to be printed: outputArray
    if numOfTrues >= numOfFalses:
        for y in range(0, (LENGTH-1)):
            for x in range(0, LANENUM):
                outputArray[y][x] = imageToGel.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
                if outputArray[y][x] == False:
                    #  add information for primers in each lane
                    primerPairInfoList[x] += "\n"
                    primerPairInfoList[x] += distanceToPrimerPairLinear.rawDistToPrimerPair(y)
                    numOfFalses += 1
    else:
        for y in range(0, (LENGTH-1)):
            for x in range(0, LANENUM):
                outputArray[y][x] = imageToGel.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
                if outputArray[y][x] == True:
                    #  add information for primers in each lane
                    primerPairInfoList[x] += "\n"
                    primerPairInfoList[x] += distanceToPrimerPairLinear.rawDistToPrimerPair(y)
                    numOfFalses += 1

    f = open("protocol.txt", "a")
    # removing contents of protocol.txt
    f.truncate(0)
    # storing protocol in protocol.txt
    for x in range(0, LANENUM):
        print("Primer info for lane #", end = '', file = f)
        print(x, end = '', file = f)
        print(" is:", file = f)
        if len(primerPairInfoList[x]) == 0:
            print("\n", file = f)
            print(' Leave this lane empty.', file = f)
            print("\n", file = f)    # return primerPairInfoList

        else:
            print("\n", file = f)
            print(primerPairInfoList[x], file = f) 
            print("\n", file = f)
    f.close()


Builder.load_string("""
<DisplayBox>:
    id: my_widget
    FileChooserListView:
        id: filechooser
        on_selection: my_widget.selected(filechooser.selection)
    Image:
        id: image
        source: ""
""")


class DisplayBox(BoxLayout):

    def selected(self,filename):
        try:
            self.ids.image.source = filename[0]
            imagePath = filename[0]
            print(imagePath)
            primerPairInfoList(imagePath) # fix protocol.txt
            imageToGel.printImage(imagePath) # print gel image
        except:
            pass


class PictureBoxUpdateProtocol(App):
    def build(self):
        return DisplayBox()


if __name__ == '__main__':
    PictureBoxUpdateProtocol().run()