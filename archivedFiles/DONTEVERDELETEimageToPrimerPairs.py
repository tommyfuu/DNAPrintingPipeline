
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
import imageToGel, distanceToPrimerPair

def primerPairInfoList():
    # image 
    image1 = './test2.jpeg'

    # intialise things
    outputArray = [[False] * 20] * 39
    im = PIL.Image.open(image1)
    imgwidth, imgheight = im.size
    boxHeight = imgheight//39
    boxWidth = imgwidth//20
    standard = imageToGel.standardBrightness(im)

    primerPairInfoList = ["Primer Info: "]*20
    # array to be printed: outputArray
    for y in range(0, 39):
        for x in range(0, 20):
            outputArray[y][x] = imageToGel.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
            if outputArray[y][x] == False:
                # 1. find the distance ratio
                tempDistRatio = y/39
                # 2. use the log formula to get the desired sequence length
                rawSeqLength = -0.641-2.41*np.log(tempDistRatio)
                # 3. add information for primers in each lane
                primerPairInfoList[x] += "\n"
                primerPairInfoList[x] += distanceToPrimerPair.rawDistToPrimerPair(tempDistRatio)

    # print out primer info for each lane
    for x in range(0, 20):
        print("Primer info for lane #", end = '')
        print(x, end = '')
        print(" is:")
        print(primerPairInfoList[x])

    return primerPairInfoList