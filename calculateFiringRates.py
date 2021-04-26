import sys
def find_stim(line):
    for i in range(len(line)):
        if line[i] == 1:
            return i

def main():
    """ given: a file of stimuli generated by generateInput.py and a file
    of outputs generated by modelv6.py, calculates the firing rate of each neuron in response to the stimulus provided on the command line, or all stimuli if none provided. Specify layer 4 by adding --layer4 flag; assumes layer 2-3 otherwise.  
    """
    # get input
    args = sys.argv[1:]
    if len(args) < 2 or len(args) > 4: 
        print("usage: stimulus_file outputs_file [neuron] [--layer4]")
        sys.exit(1)
     
    stim_filename = args[0]
    output_filename = args[1]

    is_layer_four = False
    one_stim_only = False

    if len(args) >= 3:
        if args[2] == "--layer4":
             is_layer_four = True
             if len(args) == 4:
                 one_stim_only = True
                 stimulus = int(args[3])
        else:
            one_stim_only = True
            stimulus = int(args[2])
            if len(args) == 4:
                is_layer_four = True
        

    # open files
    stim_file = open(stim_filename, 'r')
    output_file = open(output_filename, 'r')

    # throw out first line (and second if layer 2/3)
    output_file.readline()
    if not is_layer_four:
        output_file.readline()
    
    # create array of firing-rate-arrays (that is, index 0 indicates stimulus 0 and index 0[0] indicates the first neuron's firing rate in response to stimulus 0)
    stim_line = [int(i) for i in stim_file.readline().split()]
    if one_stim_only:
        num_stimuli = 1
    else:
        num_stimuli = len(stim_line)
    

    out_line = [int(i) for i in output_file.readline().split(", ")]
    num_neurons = len(out_line)

    indexed_by_stim = [[0 for j in range(num_neurons)] for i in range(num_stimuli)]
    
    num_timebins_stimulus = [0 for i in range(num_stimuli)]

    # main loop
    while(stim_line and out_line[0] != ""):

        # turn the strings into lists (can't do this before checking if they're empty)
        stim_line = [int(i) for i in stim_line]
        out_line = [int(i) for i in out_line]

        # calculate which stimulus it is
        curr_stim = find_stim(stim_line)

        num_timebins_stimulus[curr_stim] += 1

        if one_stim_only:
            if curr_stim == stimulus:
                index = 0
            else: 
                index = -1
        else:
            index = curr_stim


        # add 1 to the firing rate of each neuron that fired
        if index != -1:
            indexed_by_stim[index] = [indexed_by_stim[index][i] + out_line[i] for i in range(num_neurons)]

        # update lines
        stim_line = stim_file.readline().split()
        out_line = output_file.readline().split(", ")

    for i in range(num_stimuli):
        num_stim_appeared = float(num_timebins_stimulus[i])
        print >> sys.stderr, "Stimulus %d appeared %f times" % (i, num_stim_appeared)
        print("Stimulus %d," % i, end='')
        print(", ".join(str(j/num_stim_appeared) for j in indexed_by_stim[i]))
    


if __name__ == "__main__":
  main()