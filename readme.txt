In this directory:
The main simulation: 
    - modelv6.py: the network itself. Calculates firing rates in response to stimuli provided. Outputs L4 and L23 firing rates and plots in most basic usage.  

Library files:
    - layerfuncs.py: functions related to layer objects
    - layerdefs.py: the definitions of layer objects 

Other files:
    - calculateFiringRates.py: calculates the firing rate of each neuron in layer 2/3 in response to each stimulus. With --layer4 flag, does this for layer 4. Can also calculate for a specific stimulus if given on command line.
    - generateInput.py: generates input to the model. Appends n repetitions of each stimulus vector using a hidden markov model, or random if -random specified. 
    - processWeightMatrix.py: processes weight matrices output by numpy.ndarray.tofile() into a more convenient format for MATLAB 

Sub-directories: 
    - older-versions: old files and versions no longer in use. 
    - input-files: input files. 
    - output-files: output files. 
    - plots: plots of various results. 
Each subdirectory has its own readme. 