import sys
import time
import numpy
import layerdefs as ldefs
import layerfuncs as lfuncs
import freqTesting as freq

def main():
  """ reads input_filename and output_filename from command line. 
  creates L4 object and returns the output if it always fired and the output based on the distribution given by the sigmoid function. returns the
  frequency of different neurons fired over a number of runs. 
  create L23 object and returns what fired in a given run and the frequency
  with which neurons fired over a number of runs, without recurrence. 

  input parameters are described in "usage" sections of the input file. 
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
  L4_spike_vec = lfuncs.probvec_to_spikevec(sig_out)

  print "---- Layer 4: ---- "
  print "Excitation: " + lfuncs.spikevec_toString(exc_vec)
  print "Spiked: " + lfuncs.spikevec_toString(L4_spike_vec)

  # test frequencies of firing (commented out for convenience)
  # freq.L4_freqs(n4, sig_out)

  # -------- layer 2/3 testing ------------------------
  l23 = ldefs.L23(n23, n4, mean, stdp_eta)
  spiking_input = lfuncs.spikevec_where(L4_spike_vec)

  # give L4 input to get excitation, feed to sigmoid, use probabilities to get spikes
  exc_vec = lfuncs.net_input_vector(l23.inputWeightMatrix, spiking_input)
  sig_out = lfuncs.sig_prob(exc_vec, beta, theta)
  L23_spike_vec = lfuncs.probvec_to_spikevec(sig_out)

  # write outputs to file: columns for each spiking neuron j in input, 
  # summed excitation, and sigmoid probabilities 
  file = open(output_filename, 'a')

  # commented out for convenience 
  # for j in lfuncs.spikevec_where(L4_spike_vec):
  #   j_out = [round(l23.inputWeightMatrix[i][j], 2) for i in range(len(l23.inputWeightMatrix))]
  #   file.write("\n\nj%d: %s" % (j, str(j_out)))

  # file.write("\n\nexc " + str([round(i,2) for i in exc_vec]))
  # file.write("\n\nsig " + str([round(i, 2) for i in sig_out]))
  file.write(str([round(i, 2) for i in sig_out]))
  file.close()

  print "---- Layer 2/3: ---- "
  print "Spiked: " + lfuncs.spikevec_toString(L23_spike_vec)

  # test frequencies of firing (commented out for convenience)
  # freq.L23_freqs(n23, output_filename, sig_out)

if __name__ == "__main__":
  main()