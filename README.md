# DNAPrintingPipeline

## step 1. make sure you have the right libraries downloaded
This project uses the following python library:  
Panda, PIL, numpy, math, os(operating system control)  
  
To make sure you have the right libraries downloaded, in your terminal, cd to enter the current directory (DNAPrintingPipeline), type `pip3 install -r requirements.txt`. Note that math and os should be built in python dictionaries without the need of installing.  

## step 2. get your primer pairs from input image
- Note that with the current primer pairs we have, our version 1 is currently a better option because our primer pairs give linearly spaced distances. With more primer pairs coming in and the algorithm optimised, version 2 will gradually replace version 1.  

### version 1. linearly spaced primer pairs

If you wish to change the input picture, move the picture into the current directory, rename, and make that an object in imageToPrimerPairLinear.py and imageToGel.py. Change code accordingly. An example is on lines 15-16 of imageToPrimerPairLinear.py and lines 7-8 of imageToGel.py.  

Note that we will recommend simpler pictures - better if the colours are simple.  

Enter the current directory (DNAPrintingPipeline). In the current directory, enter in the terminal `python -i imageToPrimerPairsLinear.py`. After the function call, `protocol.txt` should appear in the directory. It should contain the primer pairs for each lane to generate a certain graph on the gel. This graph should be printed to the terminal. 

### version 2. regression to reform picture on gel
If you wish to change the input picture, move the picture into the current directory, rename, and make that an object in imageToPrimerPairs.py, change code accordingly. An example is on lines 15-16 of imageToPrimerPairs.py.  

Note that we will recommend simpler pictures - better if the colours are simple.  

Enter the current directory (DNAPrintingPipeline). In the current directory, enter in the terminal `python -i imageToPrimerPairs.py`, and then inside python, type `primerPairInfoList()`. This will let you know the primer pairs for each lane to generate a certain graph on gel.  

Regression can be find on tab 2 of [this spreadsheet](https://docs.google.com/spreadsheets/d/1KOYfS4cVNAYSwTB1CCfx9eiYY1d4YHv_HNWY8ircnPc/edit?usp=sharing) - note that this spreadsheet is only accessible to people inside the Harvey Mudd gsuite  

## Future optimisation
1. Better resolution
2. Enable more flexible gel dimension (currently 20\*40)
3. More primer pair info to enable better regression


## Acknowledgement
The image analysis part of thie pipeline is done with the generous help of [Bowen](https://github.com/JiangBowen0008). Some source files are from [Roya](https://github.com/ramininaieni) and [Max](https://github.com/maxschommer).

Enjoy,
TF
