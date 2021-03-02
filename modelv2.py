import sys
import time
import numpy
import layerdefs as ldefs
import layerfuncs as lfuncs

def main():
  """ reads input_filename from command line. 
  creates L4 object and returns the output if it always fired and the output based on the distribution given by the sigmoid function. 

  input should have the format: line 1 - n4 (number of neurons in layer 4), L (number of stimuli), k (neurons that respond per stimuli), beta (for sigmoid), theta (firing threshold). optional: non_k (the value to initialize neurons that don't respond to the stimuli, default -1) and random (true/false, whether the initialization should be randomized, default False). separated by whitespace. 
  line 2 - stimuli represented by 1's if present, 0's otherwise. separated by whitespace.
  line 3 onward - not read by program. 
  """

  # -------- input ------------------------
  # get command line arguments into args array
  args = sys.argv[1:] 
  if not args or len(args) > 2: 
    print "usage: input_filename output_filename"
    sys.exit(1) 
  
  input_file = open(args[0], 'r')
  output_filename = args[1]

  # get parameters separately 
  params = (input_file.readline()).split()
  if len(params) > 10:
    print "usage: n23 mean stdp_eta n4 L k beta theta [non-k] [random]"
    sys.exit(1)
  
  n23 = int(params[0])
  mean = float(params[1])
  stdp_eta = float(params[2])
  n4 = int(params[3])
  L = int(params[4])
  k = int(params[5])
  beta = float(params[6])
  theta = float(params[7])

  non_k = -1
  rand = False

  if len(params) > 5:
    non_k = float(params[8])
    if len(params) > 6:
      rand = params[9]

  # get stimuli into array 
  stimuli = input_file.readline() 
  stimuli = [int(i) for i in stimuli.split()]
  stimuli = numpy.array(stimuli)
  
  if len(stimuli) != L:
    print "error! there must be %d stimuli" % L
    sys.exit(1)

  # -------- layer 4 testing ------------------------
  # create L4 object
  l4 = ldefs.L4(n4, L, k, randomize=rand, non_k=non_k)

  # print output vector of neurons that fired: 
  exc_vec = lfuncs.excitation(l4, stimuli)
  sig_out = lfuncs.sig_prob(exc_vec, beta, theta)
  spike_vec = lfuncs.probvec_to_spikevec(sig_out)

  print "---- Layer 4: ---- "
  print "Excitation: " + lfuncs.spikevec_toString(exc_vec)
  print "Spiked: " + lfuncs.spikevec_toString(spike_vec)

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

  # -------- layer 2/3 testing ------------------------
  l23 = ldefs.L23(n23, n4, mean, stdp_eta)
  exc_vec = lfuncs.net_input_vector(l23)
  sig_out = lfuncs.sig_prob(exc_vec, beta, theta)
  spike_vec = lfuncs.probvec_to_spikevec(sig_out)

  print "---- Layer 2/3: ---- "

  print "Spiked: " + lfuncs.spikevec_toString(spike_vec)

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
  out = open(output_filename, 'a') 
  out.write("Trials: %d" % execs)
  out.write("expected \tactual\t difference\n")

  for i in range(len(sig_out)):
    expected = (sig_out[i] * execs)

    out.write(str(expected) + "\t")
    out.write(str(freqs[i]) + "\t")

    diff = expected - freqs[i]
    diff_sum += diff

    out.write(str(diff) + "\n")

  diff_mean = float(diff_sum)/float(n23)

  out.write("Difference column mean: %f" % diff_mean)
  out.close() 
  print "Difference column mean: %f" % diff_mean


if __name__ == "__main__":
  main()