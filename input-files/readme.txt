This directory contains input files to the programs in the main directory. 
The directory consists of these subdirectories:
    - modelv1_format: input files in the format used by modelv1.py, with one line of parameters and one line of a stimulus. Name pattern: input[1-9][rand].txt.
    - modelv4_format: input files in the format used by modelv4.py, with more parameters and one line of a stimulus. Name pattern: in[1-9][rand].txt. 
    - stims: entire stimulus files, which could be the stimulus filename given to modelv6.py. Usually generated by generateInput.py. Name pattern: [rand / hmm]-[number of lines]-[date generated].txt. 
    - vecs: stimulus vectors, one line each. For example, vec1.txt is "1 0 0 0 0 0 0 0 0." vec1-rep[n] contains that many repetitions of the vector. Usually used by generateInput.py. 

In the directory itself are parameter files which can be used by modelv6.py as command-line arguments. 