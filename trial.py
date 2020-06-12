"""
Author      : Tom Fu
Date        : 2020 April 8
Description : trial.py for DNA Printing Project
"""
# imports for DNAPrinting
import numpy as np
import PIL.ImageStat
import PIL.Image
import math
import os
import imageToGel, distanceToPrimerPairLinear

import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty


############### DNA Printing Functions ###############


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

############### Kivy GUI part ###############

Builder.load_string("""
<FirstScreen>:
    BoxLayout:
        orientation: "horizontal"
        FloatLayout:
            Label:
                id: first_screen_label
                text: "HMC DNA Printing Station"
                pos_hint: {'top': 1.2}
            Image:
                pos_hint: {'top': 1}
                source: "/Users/apple/Desktop/DNAPrintingPipeline/DNAPrinting.png"

        BoxLayout:
            orientation: "vertical"
            Button:
                text: "Select your picture to print!"
                background_color: 0.5, 0.8, 0.6, 1
                on_press: root.manager.current = '_second_screen_'
            Button:
                text: "Cancel!"
                on_press: app.stop()

<SecondScreen>:
    id: file_chooser
    Widget:
        id: file_chooser_box_layout
        Label:
            id: notice
            text: "Note that you should only select image files (e.g.: png/jpeg/etc.)"
            pos: 340, 480
        Button
            text: "select this image"
            size: 300, 50
            pos: 270, 20
            on_press: 
                root.callback_image_and_other_stuff(file_chooser_list_view.selection)
        FileChooserListView:
            id: file_chooser_list_view
            size: 450, 430
            pos: 170, 70

<ThirdScreen>:
    BoxLayout:
        orientation: "vertical"
        id: third_screen
        Label:
            id: main_title
            text: "Are you sure you want this image?"
            size_hint: (1, 0.1)
        Image:
            id: main_image
            source: root.img
            size_hint: (1, 0.75)
        BoxLayout:
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                text: "Okay"
                size_hint: (0.5, 1)
                on_press: root.manager.current = '_fourth_screen_'
            Button:
                text: "Cancel"
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_' 

<FourthScreen>:
    BoxLayout:
        orientation: "vertical"
        id: third_screen
        Label:
            id: main_title
            text: "Previewing protocol"
            size_hint: (1, 0.1)
        Image:
            id: preview_image
            source: root.img
            size_hint: (1, 0.75)
        BoxLayout:
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                text: "Okay"
                size_hint: (0.5, 1)
                on_press: image_viewer.image_accepted_by_user(filechooser.selection)
            Button:
                text: "Cancel"
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_'  
""")

class FirstScreen(Screen):
    pass

class SecondScreen(Screen):
    def callback_image_and_other_stuff(self, new_image_address):
        if new_image_address:
            third_screen = self.manager.get_screen("_third_screen_")
            # do other stuff here also, then pass new_image_address along
            new_image_address = new_image_address[0].replace("\\", "/")
            third_screen.callback_image(new_image_address)

class ThirdScreen(Screen):
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def callback_image(self, new_image_address):
        sm.current = "_third_screen_"
        self.img = new_image_address
        self.ids.main_image.source = self.img
        primerPairInfoList(new_image_address) # fix protocol.txt
        imageToGel.printImage(new_image_address) # print gel image
        print(self.img)

class FourthScreen(Screen):
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        

    def callback_image4(self, new_image_address):
        sm.current = "_fourth_screen_"
        self.img = new_image_address
        self.ids.main_image.source = self.img
        print(self.img)

# Create the screen manager
sm = ScreenManager() # Problem?
sm.add_widget(FirstScreen(name='_first_screen_'))
sm.add_widget(SecondScreen(name='_second_screen_'))
sm.add_widget(ThirdScreen(name='_third_screen_'))
sm.add_widget(ThirdScreen(name='_fourth_screen_'))

class MyApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()