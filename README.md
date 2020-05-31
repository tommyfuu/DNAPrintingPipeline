# DNAPrintingPipeline

## May 31, 2020 Update - Simple GUI implemented
In today's update, Tom implemented a simple GUI with Kivy that allows the users to pick a picture from their system directory, and the protocol.txt will become the protocol containing necessary and minimum amount of primer pairs used. In terminal, it will also print out the matched gel image - with minimum amount of primer pairs used as well.

### step 1. make sure you have the right libraries downloaded
This project uses the following python library:  
Panda, PIL, numpy, math, os(operating system control)  

To make sure you have the right libraries downloaded, in your terminal, cd to enter the current directory (DNAPrintingPipeline), type `pip3 install -r requirements.txt`. Note that math and os should be built in python dictionaries without the need of installing.  

### step 2. run the GUI

To run this GUI, clone this repository and enter the directory. In the terminal, enter `python trialPictureBox.py`. A Kivy viewing panel should pop up. On the left-hand side of the window, click and go to the address where your desired image is located. Click on the image, then by the time you see your pixelised image in terminal, the output protocol.txt will contain the necessary primer pairs you need already. Yayy!

Note that we will recommend simpler pictures - better if the colours are simple.  

### Future optimisation
- GUI:
1. Allow manual adjustments on the 20*40 gels
2. Aesthetics
- DNA Printing
1. Better resolution
2. Enable more flexible gel dimension (currently 20\*40)
3. More primer pair info to enable better regression


### Acknowledgement
The image analysis part of thie pipeline is done with the generous help of [Bowen](https://github.com/JiangBowen0008). Some source files are from [Roya](https://github.com/ramininaieni) and [Max](https://github.com/maxschommer).

Enjoy,
TF
