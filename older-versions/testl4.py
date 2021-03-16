from l4 import L4 
import sys
import numpy
import time

def toVector(filename):
    vec = numpy.array([int(i) for i in ((open(filename, 'r')).read()).split()])
    return vec

def main(): 
    # read number of neurons from command line 
    args = sys.argv[1:]
    if not args:
        print "usage: number_of_neurons [extra_input_files]"
        sys.exit(1)
    
    n = int(args[0])
    if len(args) > 1:
        filenames = args[1:]
    else:
        filenames = ""

    # INITIALIZATION TESTS
    print "---- Initialization Tests ----"

    #  TEST 1: create an L4 object 
    layer = L4(n)
    print "Test 1: Initialize object. Passed."

    # TEST 2: check L
    result = ""
    if layer.L == 9: 
        result = " Passed."
    else:
        result = " Failed."
    
    print "Test 2: L = 9.%s" % result 

    # TEST 3: check firePerStim
    if layer.firePerStim == 4:
        result = " Passed."
    else:
        result = " Failed."

    print "Test 3: firePerStim = 4.%s" % result

    # TEST 4: check n4
    if layer.n4 == n:
        result = " Passed."
    else:
        result = " Failed."

    print "Test 4: n = %d.%s" % (n, result)

    # TEST 5: check if firePerStim neurons respond to each stimulus
    result = " Passed."

    for j in range(layer.L):
        ct = 0
        for i in range(layer.n4):
            if layer.weightMatrix[i][j] == 1:
                ct += 1
        if ct != layer.firePerStim:
            print "Too many neurons respond to stimulus %d" % j
            result = " Failed."

    print "Test 5: firePerStim neurons respond to each stimulus.%s" % result
        
   # TEST 6: generate multiple objects and check if the distribution of neurons in the weightMatrix is plausible 
    print "Test 6: PLACEHOLDER"

    # TEST OUTPUT
    print "---- Output Tests ----"

    # Input files 
    if (filenames):
        print "INPUT FILES: PLACEHOLDER"
    
    # File 1: input.txt
    t0 = time.time()
    freqs = [0 for i in range(layer.n4)]
    in1 = toVector("input.txt")
    if len(in1) != layer.L:
        print "error: there must be %d stimuli" % l4.L
        sys.exit(1)

    for i in range(100):
        temp = L4(n)
        alwaysVec = temp.always_fire(in1)
        alwaysWhere = temp.fire_out_where(alwaysVec)
        for j in alwaysWhere:
            freqs[j] += 1
    
    print freqs
    # what now? testing random in put is hard
    t1 = time.time()
    print "Time: %f" % (t1-t0)



if __name__ == "__main__":
  main()