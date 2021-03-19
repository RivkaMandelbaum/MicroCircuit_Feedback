import layerfuncs as lfuncs
import time 
import os

def print_L4_freqs(n4, sig_out):
    # print distribution of spikes over execs trials given fixed probability
    # and timing
    start_time = time.clock()

    freqs = [0 for nrn in range(n4)]
    execs = 100
    for i in range(execs):
        spike_vec = lfuncs.probvec_to_spikevec(sig_out)
        for nrn in lfuncs.spikevec_where(spike_vec):
            freqs[nrn] += 1
    end_time = time.clock() 

    print "Frequencies: " + str(freqs)
    print "Time for %d executions: %f sec" % (execs, end_time-start_time)

def write_L4_freqs(n4, sig_out, output_filename, mode='w', execs=100):
    """ outputs firing rates of neurons in format readable by MATLAB
    """
    freqs = [0 for nrn in range(n4)]
    for i in range(execs):
        spike_vec = lfuncs.probvec_to_spikevec(sig_out)
        for nrn in lfuncs.spikevec_where(spike_vec):
            freqs[nrn]+=1
    
    out = open(output_filename, mode)
    # out.write(os.path.basename(output_filename) + ": ")
    for f in freqs:
        out.write("%d, " % f)
    out.write('\n')
    out.close()

def write_L23_freqs(n23, vec, output_filename, mode = 'w', execs=100, recalc_L4 = False, recalc_L23 = False):
    """ writes firing rates of neurons in L23 after recurrent activity in format readable by MATLAB, to output_filename. Runs a default of 100 times. 
    Overwrites file by default, but mode can be specified. 
    If recalc_L4 and recalc_L23 are false, vec should be a sig_out vector representing probability of L23 recurrent layer firing. (Default case).
    If recalc_L23 is true but recalc_L4 is false, vec should be an L4 spike 
    vector. 
    If recalc_L4 is true, recalc_L23 must be true and vec should be a sig_out
    vector representing probability of firing in L4.  
    """
    if recalc_L4 and not recalc_L23: 
        print "Error: if L4 is recalculated, L23 must be recalculated"

    freqs = [0 for nrn in range(n23)]
    for i in range(execs):
        spike_vec = lfuncs.probvec_to_spikevec(vec)
        for nrn in lfuncs.spikevec_where(spike_vec):
            freqs[nrn]+=1
    
    out = open(output_filename, mode)
    # out.write(os.path.basename(output_filename) + ", ")
    for f in freqs:
        out.write("%d, " %f)
    out.write('\n')
    out.close()

def check_L23_freqs(n23, output_filename, sig_out, mode='w', execs=100):
    """ prints the firing rates of each neuron over a number of trialss
    specified by execs (default 100), based on the sig_out probability vector and n23. also prints time taken to calculate. 
    Writes actual vs. expected firing rates and the difference between them
    to the file specified by output_filename, with default mode = 'w'.
    Also writes mean of difference column, and prints it. 
    """
    # print distribution of spikes over execs trials given fixed probability
    # and timing
    start_time = time.clock()

    freqs = [0 for nrn in range(n23)]
    for i in range(execs):
        spike_vec = lfuncs.probvec_to_spikevec(sig_out)
        for nrn in lfuncs.spikevec_where(spike_vec):
            freqs[nrn] += 1
    end_time = time.clock() 

    print "Frequencies: " + str(freqs)
    print "Time for %d executions: %f sec" % (execs, end_time-start_time)
    
    # append real frequency vs. expected to output file
    diff_sum = 0
    out = open(output_filename, mode) 
    out.write("Trials: %d\n" % execs)
    out.write("expected \tactual\t difference\n")

    for i in range(len(sig_out)):
        expected = int(round((sig_out[i] * execs)))

        out.write(str(expected) + "\t")
        out.write(str(freqs[i]) + "\t")

        diff = expected - freqs[i]
        diff_sum += diff

        out.write(str(diff) + "\n")

    diff_mean = float(diff_sum)/float(n23)

    out.write("Difference column mean: %f" % diff_mean)
    out.close() 
    print "Difference column mean: %f" % diff_mean

def compare_L23_rates(n23, output_filename, sig_out, rec_sig_out, mode='a', execs = 100):
    """ compares the firing rates of neurons based on the two weight
    matrices in L23, using the probability vectors sig_out and rec_sig_out
    and the quantity n23. writes to file specified by output_filename the number
    of trials (execs, default 100), then one line for each neuron, with
    firing rate into recurrent connection and firing rate after recurrence. 
    by default, this appends to file, but mode can be specified. 
    """
    freqs = [0 for nrn in range(n23)]
    rec_freqs = [0 for nrn in range(n23)]
    execs = 100
    for i in range(execs):
        spike_vec = lfuncs.probvec_to_spikevec(sig_out)
        rec_spike_vec = lfuncs.probvec_to_spikevec(rec_sig_out)
        for nrn in lfuncs.spikevec_where(spike_vec): 
            freqs[nrn] += 1
        for nrn in lfuncs.spikevec_where(rec_spike_vec):
            rec_freqs[nrn] += 1
    
    out = open(output_filename, mode)
    out.write("Trials:%d\n" % execs)
    out.write("freqs rec_freqs\n")
    for i in range(len(sig_out)):
        out.write("%d, " % freqs[i])
        out.write("%d\n" % rec_freqs[i])
    out.close()

# def main():
  

# if __name__ == "__main__":
#   main()