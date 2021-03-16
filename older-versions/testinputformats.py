def main():
    """ reads in parameters from input file provided on command line and prints them back out. just for testing how to work with different input file formats. """ 
     # get command line arguments into args array
    args = sys.argv[1:] 
    if not args or len(args) > 1: 
        print "usage: input_filename"
        sys.exit(1) 
    
    input_file = open(args[0], 'r')
    # get parameters separately 
    params = (input_file.readline()).split()
    if len(params) > 7:
        print "usage: n4 L k beta theta [non-k] [random]"
        sys.exit(1)

    n4 = int(params[0])
    L = int(params[1])
    k = int(params[2])
    beta = int(params[3])
    theta = int(params[4])

    non_k = -1
    rand = False

    if len(params) > 5:
        non_k = int(params[5])
        if len(params) > 6:
        rand = params[6]

    # get stimuli into array 
    stimuli = input_file.readline() 
    stimuli = [int(i) for i in stimuli.split()]
    stimuli = numpy.array(stimuli)
    
    if len(stimuli) != L:
        print "error! there must be %d stimuli" % L
        sys.exit(1)

if __name__ == "__main__":
  main()