import sys
import time
import numpy
import layerdefs as ldefs
import layerfuncs as lfuncs
import freqTesting as freq
import os

def main():
  """ reads input_filename and output_filename from command line. 
  creates L4 object and returns the output if it always fired and the output based on the distribution given by the sigmoid function. returns the
  frequency of different neurons fired over a number of runs. 
  create L23 object and returns what fired in a given run and the frequency
  with which neurons fired over a number of runs, after including recurrence. 

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
  L4_exc_vec = lfuncs.excitation(l4, stimuli)
  L4_sig_out = lfuncs.sig_prob(L4_exc_vec, beta, theta)
  L4_spike_vec = lfuncs.probvec_to_spikevec(L4_sig_out)

  print "---- Layer 4: ---- "
  print "Excitation: " + lfuncs.spikevec_toString(L4_exc_vec)
  print "Spiked: " + lfuncs.spikevec_toString(L4_spike_vec)

  # test frequencies of firing (commented out for convenience)
  # freq.print_L4_freqs(n4, L4_sig_out)
  #freq.write_L4_freqs(n4, L4_sig_out, output_filename, mode='a')

  # -------- layer 2/3 testing ------------------------
  l23 = ldefs.L23(n23, n4, mean, stdp_eta)
  L4_spiking_input = lfuncs.spikevec_where(L4_spike_vec)

  # give L4 input to get excitation, feed to sigmoid, use probabilities to get spikes from input weight matrix
  L23_exc_vec = lfuncs.net_input_vector(l23.inputWeightMatrix, L4_spiking_input)
  L23_sig_out = lfuncs.sig_prob(L23_exc_vec, beta, theta)
  L23_spike_vec = lfuncs.probvec_to_spikevec(L23_sig_out)

  # give L23 input layer spikes to get excitation, to sigmoid, to spikes of L23 after recurrence
  L23_spiking_input = lfuncs.spikevec_where(L23_spike_vec)
  L23r_exc_vec = lfuncs.net_input_vector(l23.recurrentWeightMatrix, L23_spiking_input)
  L23r_sig_out = lfuncs.sig_prob(L23r_exc_vec, beta, theta)
  L23r_spike_vec = lfuncs.probvec_to_spikevec(L23r_sig_out)

  print "\n---- Layer 2/3: ---- "
  print "First layer:"
  print "%d neurons spiked:\n%s\n" % (len(lfuncs.spikevec_where(L23_spike_vec)), lfuncs.spikevec_toString(L23_spike_vec))
  print "Recurrent layer:"
  print "%d neurons spiked:\n%s" % (len(lfuncs.spikevec_where(L23r_spike_vec)), lfuncs.spikevec_toString(L23r_spike_vec))


  # test frequencies of firing (commented out for convenience)
  #freq.check_L23_freqs(n23, output_filename, L23_sig_out)
  #freq.check_L23_freqs(n23, output_filename, L23r_sig_out, mode ='a')
  #freq.compare_L23_rates(n23, output_filename, L23_sig_out, L23r_sig_out, mode='w')
  #freq.write_L23_freqs(n23, L23r_sig_out, output_filename, mode='a')

  execs = 100
  mode = 'a'
  freqs = [0 for nrn in range(n23)]
  for i in range(execs):
    L4_spike_vec = lfuncs.probvec_to_spikevec(L4_sig_out)
    L23_exc_vec = lfuncs.net_input_vector(l23.inputWeightMatrix, L4_spiking_input)
    L23_sig_out = lfuncs.sig_prob(L23_exc_vec, beta, theta)
    L23_spike_vec = lfuncs.probvec_to_spikevec(L23_sig_out)
    L23_spiking_input = lfuncs.spikevec_where(L23_spike_vec)
    L23r_exc_vec = lfuncs.net_input_vector(l23.recurrentWeightMatrix, L23_spiking_input)
    L23r_sig_out = lfuncs.sig_prob(L23r_exc_vec, beta, theta)
    L23r_spike_vec = lfuncs.probvec_to_spikevec(L23r_sig_out)
    for nrn in lfuncs.spikevec_where(L23r_spike_vec):
      freqs[nrn]+=1
    
  out = open(output_filename, mode)
  out.write(os.path.basename(args[0]) + ", ")
  for f in freqs:
    out.write("%d, " % f)
  out.write('\n')
  out.close()



if __name__ == "__main__":
  main()