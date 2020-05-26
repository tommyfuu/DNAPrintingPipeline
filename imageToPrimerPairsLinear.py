
"""
Author      : Tom Fu
Date        : 2020 April 8
Description : imageToPrimerPairs.py for DNA Printing Project
"""
import numpy as np
import PIL.ImageStat
import PIL.Image
import math
import os
import imageToGel, distanceToPrimerPairLinear

def primerPairInfoList():
    # image 
    image1 = './dna-vector-icon.jpg'

    # intialise things
    outputArray = [[False] * 20] * 39
    im = PIL.Image.open(image1)
    imgwidth, imgheight = im.size
    boxHeight = imgheight//39
    boxWidth = imgwidth//20
    standard = imageToGel.standardBrightness(im)

    primerPairInfoList = [""]*20
    # array to be printed: outputArray
    for y in range(0, 39):
        for x in range(0, 20):
            outputArray[y][x] = imageToGel.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
            if outputArray[y][x] == False:
                #  add information for primers in each lane
                primerPairInfoList[x] += "\n"
                primerPairInfoList[x] += distanceToPrimerPairLinear.rawDistToPrimerPair(y)
    f = open("protocol.txt", "a")
    # removing contents of protocol.txt
    f.truncate(0)
    # storing protocol in protocol.txt
    for x in range(0, 20):
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
primerPairInfoList()
# printing image as confirmation of protocol
imageToGel.main()
