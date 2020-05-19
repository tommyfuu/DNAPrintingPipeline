# DNAPrintingPipeline

### version 1. linearly spaced primer pairs
To run this code, download/clone the current directory, in the current directory, enter in the terminal `python -i imageToPrimerPairLinear.py`, and then inside python, type `primerPairInfoList()`. This will let you know the primer pairs for each lane to generate a certain graph on gel.

### version 2. regression to reform picture on gel
To run this code, download/clone the current directory, in the current directory, enter in the terminal `python -i imageToPrimerPairs.py`, and then inside python, type `primerPairInfoList()`. This will let you know the primer pairs for each lane to generate a certain graph on gel.

### Picture selection
If you wish to change the input picture, move the picture into the current directory, rename, and make that an object in imageToPrimerPairs.py, change code accordingly.
Note that we will recommend simpler pictures - better if the colours are simple.

The image analysis part of thie pipeline is done with the generous help of [Bowen](https://github.com/JiangBowen0008). Some source files are from [Roya](https://github.com/ramininaieni) and [Max](https://github.com/maxschommer).

### Future optimisation
1. Better resolution
2. Enable more flexible gel dimension (currently 20\*40)
3. More primer pair info to enable better regression
