import PIL.ImageStat
import PIL.Image
import math
import os


##test images
image1 = '/Users/apple/Desktop/testimagePackman.jpeg'

def calculateAverage(im, x0, x1, y0, y1):
    sumBrightness = 0 #initiate sum
    numberofpixels = 0 #initiate number of pixels
    rgb_im = im.convert('RGB')

    for x in range(x0, x1):
        for y in range(y0, y1):
            numberofpixels += 1
            r,g,b = rgb_im.getpixel((x, y))
            sumBrightness+=math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

    return sumBrightness/numberofpixels


#find perceived brightnes as a standard
##later could be compared to and decide whether the designated block would be inked or not
def standardBrightness(im):
    imgWidth, imgHeight = im.size
    
    return calculateAverage(im, 0, imgWidth, 0, imgHeight)


#find the designated block, check whether its brightness is higher than the standard
## if yes return a true; otherwise false
def processBlock(img, _x, _boxWidth, _y, _boxHeight, _standard):
    
    blockBrightness = calculateAverage( img,
                                        _x * _boxWidth ,
                                        (_x + 1) * _boxWidth -1,
                                        _y * _boxHeight,
                                        (_y + 1) * _boxHeight -1)
    # print(_x,",",_y,":",blockBrightness,":",_standard)
    #compare with standard
    return blockBrightness > _standard

if __name__ == "__main__":
    #read image
    
    im = PIL.Image.open(image1)

    #find perceived brightnes as a standard
    ##later could be compared to and decide whether the designated block would be inked or not
    standard = standardBrightness(im)
    print("Standard")
    print(standard)

    #initiate array to prepare storage, in output each block should be true or false
    ## true means inked; false means not inked

    #Parametrisation
    imgwidth, imgheight = im.size
    boxHeight = imgheight//39
    boxWidth = imgwidth//20

    outputArray = [[False] * 20] * 39

    #for loop that produces the output array: each block should have its right true or false
    #for i,j:
    for y in range(0, 39):
        for x in range(0, 20):
            outputArray[y][x] = processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
            # print(outputArray[x][y])
            if outputArray[y][x] == True:
                print("[X]", end = '')
            else:
                print("[ ]", end = '')
        print()
    
