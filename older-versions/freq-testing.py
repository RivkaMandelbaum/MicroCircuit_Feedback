import layerfuncs as lfuncs
import time 

def L4_freqs(n4, sig_out):
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

def L23_freqs(n23, output_filename, sig_out):
    # print distribution of spikes over execs trials given fixed probability
    # and timing
    start_time = time.clock()

    freqs = [0 for nrn in range(n23)]
    execs = 100
    for i in range(execs):
        spike_vec = lfuncs.probvec_to_spikevec(sig_out)
        for nrn in lfuncs.spikevec_where(spike_vec):
            freqs[nrn] += 1
    end_time = time.clock() 

    print "Frequencies: " + str(freqs)
    print "Time for %d executions: %f sec" % (execs, end_time-start_time)
    
    # save real frequency vs. expected 
    diff_sum = 0
    out = open(output_filename, 'w') 
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

# def main():
  

# if __name__ == "__main__":
#   main()