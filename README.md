# DNAPrintingPipeline

### version 1. linearly spaced primer pairs
To run this code, download/clone the current directory, in the current directory, enter in the terminal `python -i imageToPrimerPairLinear.py`, and then inside python, type `primerPairInfoList()`. This will let you know the primer pairs for each lane to generate a certain graph on gel.
- Note that with the limited primer pairs we have so far, this is the preferred method because our primer pairs give linearly spaced distances.

### version 2. regression to reform picture on gel
To run this code, download/clone the current directory, in the current directory, enter in the terminal `python -i imageToPrimerPairs.py`, and then inside python, type `primerPairInfoList()`. This will let you know the primer pairs for each lane to generate a certain graph on gel.
Regression can be find on tab 2 of [this spreadsheet](https://docs.google.com/spreadsheets/d/1KOYfS4cVNAYSwTB1CCfx9eiYY1d4YHv_HNWY8ircnPc/edit?usp=sharing) - note that this spreadsheet is only accessible to people inside the Harvey Mudd gsuite

### Picture selection
If you wish to change the input picture, move the picture into the current directory, rename, and make that an object in imageToPrimerPairs.py, change code accordingly.
Note that we will recommend simpler pictures - better if the colours are simple.

The image analysis part of thie pipeline is done with the generous help of [Bowen](https://github.com/JiangBowen0008). Some source files are from [Roya](https://github.com/ramininaieni) and [Max](https://github.com/maxschommer).

### Python libraries used
Panda, PIL, numpy, math, os
- Note that you MIGHT need to install panda and PIL if you don't have them already on your computer. VSCode usually comes with PIL, panda can be installed with instructions [here](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html).

### Future optimisation
1. Better resolution
2. Enable more flexible gel dimension (currently 20\*40)
3. More primer pair info to enable better regression


Enjoy,
TF
