"""
Author      : Tom Fu and Kariessa Schultz
Date        : 2020 Aug 13
Description : trial.py for DNA Printing Project
"""
# imports for DNAPrinting
import numpy as np
import PIL.ImageStat
import PIL.Image
import math
import os, sys
import imageToGel, imageToGelText, distanceToPrimerPairLinear, txtToPng

# GUI app
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

import queue


############### DNA Printing Functions ###############


# DNA Printing global variables
imagePath = ""
LENGTH = 39
LANENUM = 20
GELSIMPREVIEW = "./byProducts/gelSimulation.png"
PRIMERSAVEFILE = "./output/protocol.txt"

def generateProtocol(image1):
    print("LANENUM: " + str(LANENUM))
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

    print("Contents of GelSimulation.txt:")

    with open("./byProducts/gelSimulation.txt") as f:
        print(f.read())


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

Builder.load_string("""
<FirstScreen>:
    BoxLayout:
        orientation: "horizontal"
        FloatLayout:
            Label:
                id: first_screen_label
                text: "HMC DNA Printing Station"
                font_size: 35
                font_name: './GuiFiles/Lato-Black.ttf'
                pos_hint: {'top': 1.31}
            Label:
                id: first_screen_label
                text: "Designed by:"
                font_name: './GuiFiles/Lato-Regular.ttf'
                pos_hint: {'top': 0.875}
            Label:
                id: first_screen_label
                font_name: './GuiFiles/Lato-Regular.ttf'
                text: "Tom Fu & Roya Amini-Naieni & Kariessa Schultz"
                pos_hint: {'top': 0.825}
            Image:
                pos_hint: {'top': 1.1}
                source: "./GuiFiles/DNAPrinting.png"

            Button:
                text: "Settings!"
                font_name: './GuiFiles/Lato-Bold.ttf'
                background_color: 0.5, 0.8, 0.6, 1
                pos_hint: {'top': 0.23, 'x': 0.125}
                size_hint: 0.23, 0.1
                on_press: root.manager.current = '_option_screen_'
            Button:
                text: "Select an image!"
                font_name: './GuiFiles/Lato-Bold.ttf'
                background_color: 0.5, 0.8, 0.6, 1
                pos_hint: {'top': 0.23, 'x': 0.395}
                size_hint: 0.23, 0.1
                on_press: root.manager.current = '_second_screen_'
            Button:
                text: "Cancel!"
                font_name: './GuiFiles/Lato-Bold.ttf'
                background_color: 0.5, 0.8, 0.6, 1
                pos_hint: {'top': 0.23, 'x': 0.665}
                size_hint: 0.23, 0.1
                on_press: app.stop()
<OptionScreen>:
    id: lane_option
    FloatLayout:
        Label:
            text: "Enter the number of lanes on your gel box:"
            font_size: 20
            font_name: './GuiFiles/Lato-Black.ttf'
            pos_hint: {'top': 1.25}
        Label:
            text: "Note: Your lane number should be an integer. Since the system has 39 pairs of primers prepared, your number of vertical pixels will be 40. Please choose the gel box accordingly."
            text_size: self.size
            size_hint: 0.7, 1
            font_name: './GuiFiles/Lato-Italic.ttf'
            pos_hint: {'top': 1.45, 'x': 0.13}
        TextInput:
            id: lane_number_input
            text: root.laneNum
            font_name: './GuiFiles/cour.ttf'
            size_hint: (0.1, 0.08)
            pos_hint: {'top': 0.65, 'x': 0.435}
        Label:
            id: grumpy_label
            text: ""
            markup: True
            font_name: './GuiFiles/Lato-Italic.ttf'
            pos_hint: {'top': 0.85}
        Button:
            id: return_button
            text: "Submit and Continue"
            font_name: './GuiFiles/Lato-Bold.ttf'
            background_color: 0.5, 0.8, 0.6, 1
            pos_hint: {'top': 0.275, 'x': 0.355}
            size_hint: 0.26, 0.135
            on_press: root.submit_and_continue()

<SecondScreen>:
    id: file_chooser
    Widget:
        id: file_chooser_box_layout
        Label:
            id: title
            text: "Image Selector"
            font_name: './GuiFiles/Lato-Black.ttf'
            pos: 340, 500
        Label:
            id: notice
            text: "Note that you should only select image files (e.g.: png/jpeg/etc.)"
            font_name: './GuiFiles/Lato-Italic.ttf'
            pos: 340, 470
        Button
            text: "Select This Image"
            font_name: './GuiFiles/Lato-Bold.ttf'
            background_color: 0.5, 0.8, 0.6, 1
            size: 300, 50
            pos: 270, 20
            on_press: 
                root.callback_and_format_image(file_chooser_list_view.selection)
        FileChooserListView:
            id: file_chooser_list_view
            font_name: './GuiFiles/Lato-Bold.ttf'
            size: 450, 430
            pos: 170, 70

<ThirdScreen>:
    BoxLayout:
        orientation: "vertical"
        id: third_screen
        Label:
            id: main_title
            text: "Are you sure you want this image?"
            font_name: './GuiFiles/Lato-Black.ttf'
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
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1)
                on_press: root.select_image(root.img)
            Button:
                text: "Cancel"
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_' 

<LoadingScreen>:
    BoxLayout:
        orientation: "vertical"
        id: loading_screen
        Label:
            id: loading_lable
            font_name: './GuiFiles/Lato-Black.ttf'
            text: "Loading..."
            size_hint: (1,0.1)

<FourthScreen>:
    BoxLayout:
        orientation: "vertical"
        id: fourth_screen
        Label:
            id: main_title
            text: "Previewing protocol"
            font_name: './GuiFiles/Lato-Black.ttf'
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
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1)
                on_press: root.manager.current = '_success_screen_'  
            Button:
                text: "Manual Adjustment"
                font_name: './GuiFiles/Lato-Bold.ttf'
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
            font_name: './GuiFiles/Lato-Black.ttf'
            size_hint: (1, 0.1)
            pos_hint: {'top': 1.2}
        TextInput:
            id: adjustment_text_box
            text: root.gel_simulation_text()
            font_name: './GuiFiles/cour.ttf'
            size_hint: (1, 0.75)
            pos: self.pos
        BoxLayout:
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                text: "Save and Preview"
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1)
                on_press: root.submit_text()
            Button:
                text: "Finished? Print!"
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1)
                on_press: root.manager.current = '_success_screen_'  
            Button:
                text: "Start over"
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_'

<SuccessScreen>:
    BoxLayout:
        orientation: "vertical"
        id: success_screen
        Label:
            id: main_title
            text: "Protocol generated!"
            font_name: './GuiFiles/Lato-Black.ttf'
            size_hint: (1, 0.3)
        Label:
            id: instruction
            text: "Check out protocol.txt in the output directory for PCR instruction"
            font_name: './GuiFiles/Lato-Italic.ttf'
            size_hint: (1, 0.75)
        BoxLayout:
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                text: "Close"
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1)
                on_press: app.stop()
            Button:
                text: "Do it again!"
                font_name: './GuiFiles/Lato-Bold.ttf'
                size_hint: (0.5, 1) 
                on_press: root.manager.current = '_first_screen_'  
""")

############### ScreenManager - front/back end interaction ###############

# the starting screen
class FirstScreen(Screen):
    pass

class OptionScreen(Screen):
    laneNum = str(LANENUM)
    errDisplayed = False

    def submit_and_continue(self):
        """
        (button click function)
        enter the lane number and returns; reports when the type is not integer
        """
        self.laneNum = self.ids.lane_number_input.text
        try:
            global LANENUM
            LANENUM = int(self.laneNum)
            if self.errDisplayed:
                self.errDisplayed = False
                self.ids.grumpy_label.text = ""  # resets text in case the user comes back to this page
            sm.current = "_first_screen_"
        except:
           self.errDisplayed = True
           self.ids.grumpy_label.text = '[color=ff3333]Invalid input! Please enter an integer.[/color]'
        
# the image selector screen
class SecondScreen(Screen):
    def callback_and_format_image(self, new_image_address):
        """
        (button click function)
        enter the image confirmation screen and process the image address the user inputted, so 
        it is in the right format
        """
        if new_image_address:
            third_screen = self.manager.get_screen("_third_screen_")
            # clean the address then new_image_address along
            new_image_address = new_image_address[0].replace("\\", "/")
            sm.current = "_third_screen_"
            third_screen.callback_image(new_image_address)

class ThirdScreen(Screen):
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def callback_image(self, new_image_address):
        """
        set img to the user's chosen image address
        """
        self.img = new_image_address
        self.ids.main_image.source = self.img

    def select_image(self, new_image_address):
        """ 
        (button click function)
        moves the GUI to the loading screen, which will process the chosen image
        """
        # moves the GUI to the loading screen
        loading_screen = self.manager.get_screen("_loading_screen_")
        loading_screen.img = new_image_address
        sm.current = "_loading_screen_"

# protocol previewing/simulation page
class FourthScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_pre_enter(self):
        """
        reload image so the right image is displayed
        """
        self.ids.preview_image.source = GELSIMPREVIEW
        self.ids.preview_image.reload()

    def callback_and_process_image(self, input_image):
        """
        (button click function)
        called for manual adjustment, prep for manual adjustment by forming a text file that users
        can adjust
        """
        imageToGelText.printImage(input_image, "./byProducts/gelSimulation.txt", LANENUM)  # print gel image into the text file
        generateProtocol(input_image)  # generate the right protocol.txt and gelSimulation.png

        sm.current = "_fourth_screen_"

# transition screen between selecting image and previewing the result
class LoadingScreen(Screen):
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        # calls the computationally intensive functions to process the image
        # callback_and_process_image transitions to the fourht screen when done
        fourth_screen = self.manager.get_screen("_fourth_screen_")
        fourth_screen.callback_and_process_image(self.img)  

# manual adjustment page
class AdjustmentScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        """
        reloads text so the correct text is displayed for the current file
        """
        self.ids.adjustment_text_box.text = self.gel_simulation_text()

    def enter(self):
        sm.current = "_adjustment_screen_"
        adjustment_screen = self.manager.get_screen("_adjustment_screen_")
    
    def gel_simulation_text(self):
        with open("./byProducts/gelSimulation.txt") as f:
            return f.read()

    def submit_text(self):
        """
        save the manually adjusted texts into the gelSimulation.txt file
        """
        self.adjusted_text = self.adjustment_text.text
        self.save_and_edit()
        self.adjusted_text = ''

        sm.current = "_fourth_screen_"

    def save_and_edit(self):
        with open("./byProducts/gelSimulation.txt", "w") as fobj:
            fobj.write(str(self.adjusted_text))
        manualAdjustment("./byProducts/gelSimulation.txt")

# success screen
class SuccessScreen(Screen):
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        

# Create the screen manager
sm = ScreenManager()
sm.add_widget(FirstScreen(name='_first_screen_'))
sm.add_widget(OptionScreen(name = '_option_screen_'))
sm.add_widget(SecondScreen(name='_second_screen_'))
sm.add_widget(ThirdScreen(name='_third_screen_'))
sm.add_widget(FourthScreen(name='_fourth_screen_'))
sm.add_widget(LoadingScreen(name = '_loading_screen_'))
sm.add_widget(AdjustmentScreen(name='_adjustment_screen_'))
sm.add_widget(SuccessScreen(name='_success_screen_'))


############### App call ###############

class DNAPrintingApp(App):
    def build(self):
        Window.bind(mouse_pos = self.on_mouse_pos)
        return sm 

    def on_mouse_pos(self, window, pos):
        # event for when the mouse moves
        # gets the buttons on the page and then checks for collisions
        buttons = self.get_buttons(self.root.current_screen)
        for butt in buttons:
            if butt.collide_point(*pos):
                butt.border = (0,0,0,0)
            else:
                butt.border = (2,2,2,2)                

    def get_buttons(self, widget):
        # returns a list of all buttons inside a particular widget
        # uses breadth first search
        traversalQueue = queue.Queue(0)
        traversalQueue.put(widget)
        outputList = []
        while not traversalQueue.empty():
            first = traversalQueue.get()
            for child in first.children:
                traversalQueue.put(child)
            if isinstance(first, kivy.uix.button.Button):
                outputList.append(first)
        return outputList

if __name__ == '__main__':
    DNAPrintingApp().run()