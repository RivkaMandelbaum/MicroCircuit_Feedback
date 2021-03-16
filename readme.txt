In this directory:
The main simulation: 
    - modelv4.py: L4 and L23 spiking with recurrence 

Library files:
    - layerfuncs.py: functions related to layer objects
    - layerdefs.py: the definitions of layer objects 

Other files:
    - freqTesting.py: tests the firing rates over a large number of executions
    - append-usage-description.py: appends the text in usage_string_filename to all files in directory whose name matches in[0-9]+.*txt 

Sub-directories:
    - older-versions: old files and versions no longer in use, including:
    	- modelv1.py: input vector to get output of what spiked with L4 only
    	- modelv2.py:  L4 and L23 without recurrence, but L23 acts as if all L4 neurons spiked
    	- modelv3.py: L4 and L23 without recurrence; L23 uses L4 spiking as input
    - input-files: input files with parameter and stimulus vectors have the form in[0-9].txt (randomize which L4 neurons respond to which stimuli = false) or in[0-9]rand.txt (randomize = true). Stimulus vectors alone have the form vec[0-9].txt. Sub-directory L4 has input files with parameters that were needed in modelv1.py, which only relate to L4. 
    - output-files: in each sub-directory, out[0-9].txt and out[0-9]rand.txt contain the firing rates of neurons in L23 given the corresponding input file. out-all.txt has one row for each stimulus and is importable to MATLAB. L23-input-all-L4-spike corresponds to modelv2.py, which does not have recurrence in L23 and which assumes that all L4 neurons spiked. L4-only is firing rates of L4 neurons in response to stimuli with no other layers attached. L23-recurrent is firing rates of L23 after recurrence. 