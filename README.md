# DNAPrintingPipeline

This is a simple software designed so that you can print an image on gel with DNA as your ink:)

This computational pipeline is implemented into a user-friendly platform that gives you a PCR protocol to generate the DNA fragments you need for each lane in gel electrophoresis to produce the image on gel.

## Running the pipeline

### step 1. make sure you have the right libraries downloaded

This project uses the following python library:  
Panda, PIL, numpy, math, os(operating system control)

To make sure you have the right libraries downloaded, in your terminal, cd to enter the current directory (DNAPrintingPipeline), type `pip3 install -r requirements.txt`. Note that math and os should be built in python dictionaries without the need of installing.

Install kivy with `python -m pip install kivy`. Adjust `python` into `python3` according to your os.

### step 2. run the GUI

To run this GUI, clone this repository and enter the directory.

0. In the terminal, enter `python DNAPrintingStation.py`. A Kivy viewing panel should pop up. Note that our pipeline works for Mac and Linux with tested stable behaviours, but Kivy has failed before on Windows in our testing, as seen below. You might want to use Macbooks or a Linux computer if your Windows computer does not work.
   [fronPage](https://github.com/tommyfuu/DNAPrintingPipeline/blob/master/byProducts/frontPage.png)
1. In the pop up viewing panel, you should see the first screen that tells you that this is indeed our DNA printing Project software. Click on `Select your picture to print!` to enter the software.
2. You will now see an image selector tab. Select the image you want to print on gel from your system. We provide a set of pictures in the `./testImages` directory. Note that we will recommend simpler pictures in terms of colour - the image would be printed the best if there are only two colours.
3. Then you should see an image confirmation page asking you to confirm the image (currently skipped).
4. You will now see a preview of what your picture would look like on gel, with `[ ]`s representing blank space not printed with DNAs and `[X]`s representing the space printed with DNAs, such as the one below.
   [previewExample](https://github.com/tommyfuu/DNAPrintingPipeline/blob/master/byProducts/previewExample.png)
5. If you would like, click on manual adjustment to manually adjust the output gel image if you are not satisfied with the automatically generated image. Note that you should do this by deleting the blank spaces inside the brackets with `X`s, not directly typing in `X`s or deleting blank spaces. Then you should be able to preview again by clicking on the `Save adjustment-preview again` button.
6. If you are happy with the preview, click on `Happy with it? Print!` to get your protocol. Your output PCR protocol should be in the `./output` directory as a text file called `protocol.txt` which explains the primer pairs needed for each lane.
7. If you are still not happy with the preview, feel free to go back to manual adjustment again to change anything!

## Most recent update: August 12, 2020

Implemented by Kariessa and Tom, we now fixed the following bugs/problems.

1. General delay of display by one run-through.
2. Failure to display changes in the preview image for the newly manually adjusted image.
3. Failure to update the preview image across run-throughs.
4. Organisation of files and most of the code redundancy.
5. Text revision.

### Future optimisation

- GUI:

1. Fix the skipping of image confirmation page
2. Better font fix for manual adjustment page for good consistency
3. Better and cleaner close button solution
4. Aesthetics

- Theoretical parts of DNA Printing

1. Lab corroboration of the pipeline
2. Better image resolution
3. More primer pair info to enable better regression

### Acknowledgement

This project is a collaborative effort of Tom Fu, Kariessa Schultz, and Roya Amini-Naini at the Harvey Mudd College BioMakerspace.

This project is part of the intellectual property of the Harvey Mudd College BioMakerspace. Please notify the space at **tfu@g.hmc.edu** for consent before using any of the materials in this repository. Please cite us if you use our repository for academic sharing purposes.

The funding support of the Harvey Mudd College BioMakerspace comes from Harvey Mudd College Office of Community Engagement and the college's Shanahan Fund.

The image analysis part of thie pipeline is done with the generous help of [Bowen](https://github.com/JiangBowen0008). Some source files are from [Roya](https://github.com/ramininaieni) and [Max](https://github.com/maxschommer).

Cheers,\
Tom Fu on behalf of the Harvey Mudd College Biomakerspace
