"""
Author      : Tom Fu and Kariessa Schultz
Date        : 2020 April 8
Description : trial.py for DNA Printing Project
"""
# imports for DNAPrinting
import numpy as np
import PIL.ImageStat
import PIL.Image
import math
import os
import imageToGel, imageToGelText, distanceToPrimerPairLinear, txtToPng

# GUI app
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput


############### DNA Printing Functions ###############


# DNA Printing global variables
imagePath = ""
LENGTH = 39
LANENUM = 20
GELSIMPREVIEW = "./byProducts/gelSimulation.png"
PRIMERSAVEFILE = "./output/protocol.txt"

def generateProtocol(image1):
    """
    PrimerPairInfoList - takes in an image address and updates 
        the correct PCR protocol and the gel simulation image
    input: image1, an image address
    """
    # intialise things
    outputArray = [[False] * LANENUM] * (LENGTH-1) 
    im = PIL.Image.open(image1)
    imgwidth, imgheight = im.size
    boxHeight = imgheight//(LENGTH-1)
    boxWidth = imgwidth//LANENUM
    standard = imageToGelText.standardBrightness(im)
    numOfFalses = 0
    total = LANENUM*(LENGTH-1)

    primerPairInfoList = [""]*LANENUM

    # update numOfFalses
    for y in range(0, (LENGTH-1)):
        for x in range(0, LANENUM):
            outputArray[y][x] = imageToGelText.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
            if outputArray[y][x] == False:
                numOfFalses += 1
    
    numOfTrues = total - numOfFalses

    # decide whether the true blocks or false blocks will be printed with DNA,
    # and create a text file that will be later turned into an image
    if numOfTrues >= numOfFalses:
        for y in range(0, (LENGTH-1)):
            for x in range(0, LANENUM):
                outputArray[y][x] = imageToGelText.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
                if outputArray[y][x] == False:
                    #  add information for primers in each lane
                    primerPairInfoList[x] += "\n"
                    primerPairInfoList[x] += distanceToPrimerPairLinear.rawDistToPrimerPair(y)
    else:
        for y in range(0, (LENGTH-1)):
            for x in range(0, LANENUM):
                outputArray[y][x] = imageToGelText.processBlock(im, x , boxWidth, y, boxHeight, standard) #true or false
                if outputArray[y][x] == True:
                    #  add information for primers in each lane
                    primerPairInfoList[x] += "\n"
                    primerPairInfoList[x] += distanceToPrimerPairLinear.rawDistToPrimerPair(y)

    f = open(PRIMERSAVEFILE, "a")
    # removing contents of the instructions file
    f.truncate(0)
    # storing protocol of the instructions file
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

    # generate the new simulation picture to prep for previewing
    txtToPng.simulation() 

def manualAdjustment(textAddress):
    """
    manualAdjustment - takes in a text address for the manually adjusted simulation 
        and updates the protocol and produce the right simulation image
    input: textAddress, adjusted text file after manual adjustment
    """

    primerPairInfoList = [""]*LANENUM
    numOfFalses = 0  
    total = LANENUM*(LENGTH-1)

    # find the num of falses
    # falses and trues represent different pixel colors
    with open(textAddress) as fp:
        for line in fp:
            lineCopy = line
            for pixelIndex in range(0, LANENUM):
                currentMiddleIndex = pixelIndex*3+1
                if lineCopy[currentMiddleIndex] == ' ': 
                    numOfFalses += 1
    numOfTrues = total - numOfFalses

    # decide whether the true blocks or false blocks will be printed with DNA,
    # and create a text file that will be later turned into an image
    if numOfTrues >= numOfFalses:
        with open(textAddress) as fp:
            for line in fp:
                yCount = 0
                lineCopy = line
                for pixelIndex in range(0, LANENUM): # pixelIndex is x
                    currentMiddleIndex = pixelIndex*3+1
                    if lineCopy[currentMiddleIndex] == ' ': 
                        #  add information for primers in each lane
                        primerPairInfoList[pixelIndex] += "\n"
                        primerPairInfoList[pixelIndex] += distanceToPrimerPairLinear.rawDistToPrimerPair(yCount)
                yCount += 1
    else:
        with open(textAddress) as fp:
            for line in fp:
                yCount = 0
                lineCopy = line
                for pixelIndex in range(0, LANENUM):
                    currentMiddleIndex = pixelIndex*3+1
                    if lineCopy[currentMiddleIndex] == 'X': 
                        #  add information for primers in each lane
                        primerPairInfoList[pixelIndex] += "\n"
                        primerPairInfoList[pixelIndex] += distanceToPrimerPairLinear.rawDistToPrimerPair(yCount)
                yCount += 1


    f = open(PRIMERSAVEFILE, "a")
    # removing contents of instructions file
    f.truncate(0)
    # storing protocol in instructions file
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

    # generate the new simulation picture to prep for previewing
    txtToPng.simulation()

    
############### Kivy GUI part ###############

# Kivy front end global variables
# INPUT_IMAGE_ADDRESS = """

Builder.load_string("""
<FirstScreen>:
    BoxLayout:
        orientation: "horizontal"
        FloatLayout:
            Label:
                id: first_screen_label
                text: "HMC DNA Printing Station"
                pos_hint: {'top': 1.2}
            Label:
                id: first_screen_label
                text: "Designed by:"
                pos_hint: {'top': 0.8}
            Label:
                id: first_screen_label
                text: "Tom Fu & Roya Amini-Naieni & Kariessa Schultz"
                pos_hint: {'top': 0.75}
            Image:
                pos_hint: {'top': 1}
                source: "./icon/DNAPrinting.png"

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
            background_color: 0.5, 0.8, 0.6, 1
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
                on_press: root.callback_image4(INPUT_IMAGE_ADDRESS)
            Button:
                text: "Cancel"
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_' 

<FourthScreen>:
    BoxLayout:
        orientation: "vertical"
        id: fourth_screen
        Label:
            id: main_title
            text: "Previewing protocol"
            size_hint: (1, 0.1)
        Image:
            id: preview_image
            source: "./byProducts/gelSimulation.png"
            size_hint: (1, 0.75)
        BoxLayout:
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                text: "Happy with it? Print!"
                size_hint: (0.5, 1)
                on_press: root.manager.current = '_success_screen_'  
            Button:
                text: "Manual Adjustment"
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_adjustment_screen_'  

<AdjustmentScreen>:
    adjustment_text: adjustment_text_box
    BoxLayout:
        orientation: "vertical"
        id: third_screen
        Label:
            id: main_title
            text: "Manual Adjustment"
            size_hint: (1, 0.1)
            pos_hint: {'top': 1.2}
        TextInput:
            id: adjustment_text_box
            text: root.gelSimulationText()
            size_hint: (1, 0.75)
            pos: self.pos
        BoxLayout:
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                text: "Save adjustment-preview again"
                size_hint: (0.5, 1)
                on_press: root.submit_text()
            Button:
                text: "Finished? Print!"
                size_hint: (0.5, 1)
                on_press: root.manager.current = '_success_screen_'  
            Button:
                text: "Start over"
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_'

<SuccessScreen>:
    BoxLayout:
        orientation: "vertical"
        id: success_screen
        Label:
            id: main_title
            text: "Protocol generated!"
            size_hint: (1, 0.3)
        Label:
            id: instruction
            text: "Check out protocol.txt in the output directory for PCR instruction"
            size_hint: (1, 0.75)
        BoxLayout:
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                text: "Close"
                size_hint: (0.5, 1)
                on_press: root.close()
            Button:
                text: "Do it again!"
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_'  
""")

# the starting screen
class FirstScreen(Screen):
    pass

# the image selector screen
class SecondScreen(Screen):
    def callback_image_and_other_stuff(self, new_image_address):
        """
        (button click function)
        enter the image confirmation screen and update the image address the user inputted
        """
        if new_image_address:
            third_screen = self.manager.get_screen("_third_screen_")
            # do other stuff here also, then pass new_image_address along
            new_image_address = new_image_address[0].replace("\\", "/")
            third_screen.callback_image(new_image_address)

# image confirmation page (currently fastly skipped for some reason) TODO: fix this
class ThirdScreen(Screen):
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def callback_image(self, new_image_address):
        sm.current = "_third_screen_"
        self.img = new_image_address
        self.ids.main_image.source = self.img
        print(self.img)
        fourth_screen = self.manager.get_screen("_fourth_screen_")
        fourth_screen.callback_image4(new_image_address)

# protocol previewing/simulation page
class FourthScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_pre_enter(self):
        # reload image so the right image is displayed
        self.ids.preview_image.source = GELSIMPREVIEW
        self.ids.preview_image.reload()

    def on_enter(self):
        # reload image so the right image is displayed
        self.ids.preview_image.source = GELSIMPREVIEW
        self.ids.preview_image.reload()

    def callback_image4(self, input_image):
        imageToGelText.printImage(input_image)  # print gel image into the text file
        generateProtocol(input_image)  # generate the right protocol.txt and gelSimulation.png
        sm.current = "_fourth_screen_"

        imageToGelText.imageForRescanning(input_image)
        txtToPng.rescanning()

        imageToGel.printImage("./byProducts/simulationForRescanning.png")

# manual adjustment page
class AdjustmentScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        # reloads text so the correct text is displayed for the current file
        self.ids.adjustment_text_box.text = self.gelSimulationText()

    def enter(self):
        sm.current = "_adjustment_screen_"
        adjustment_screen = self.manager.get_screen("_adjustment_screen_")
    
    def gelSimulationText(self):
        with open("./byProducts/gelSimulation.txt") as f:
            return f.read()

    def submit_text(self):
        self.adjusted_text = self.adjustment_text.text
        self.saveAndEdit()
        self.adjusted_text = ''

        sm.current = "_fourth_screen_"

    def saveAndEdit(self):
        with open("./byProducts/gelSimulation.txt", "w") as fobj:
            fobj.write(str(self.adjusted_text))
        manualAdjustment("./byProducts/gelSimulation.txt")

# success screen
class SuccessScreen(Screen):
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
          
    def close(self):
        sm.current = "_success_screen_"
        success_screen = self.manager.get_screen("_success_screen_")
        App.get_running_app.stop()
        

# Create the screen manager
sm = ScreenManager()
sm.add_widget(FirstScreen(name='_first_screen_'))
sm.add_widget(SecondScreen(name='_second_screen_'))
sm.add_widget(ThirdScreen(name='_third_screen_'))
sm.add_widget(FourthScreen(name='_fourth_screen_'))
sm.add_widget(AdjustmentScreen(name='_adjustment_screen_'))
sm.add_widget(SuccessScreen(name='_success_screen_'))

class MyApp(App):
    def build(self):
        return sm
    
    def save(self, name, job):
        fob = open('c:/test.txt','w')
        fob.write(name + "\n")
        fob.write(job)
        fob.close()    

if __name__ == '__main__':
    MyApp().run()