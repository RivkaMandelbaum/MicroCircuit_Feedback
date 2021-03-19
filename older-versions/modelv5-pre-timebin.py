import sys
import time
import numpy
import layerdefs as ldefs
import layerfuncs as lfuncs
import freqTesting as freq
import os

def main():
  """ reads four filenames from command line:
        - param_filename: the file should contain input parameters, described in "usage" sections of input files. 
        - stim_filename: the file should contain stimulus vectors, one on each line. (minimum one stimulus). 
        - l4_output_filename: will put l4 firing rates in this file. 
        - l23_output_filename: will put l23 firing rates in this file. 
      
      creates L4 and L23 objects; calculates the firing rates in response to the stimuli given. each stimulus defines a separate timebin. 
  """

  # -------- input ------------------------
  # get command line arguments into args array
  args = sys.argv[1:] 
  if not args or len(args) != 4:
    print "usage: param_filename stim_filename l4_output_filename l23_output_filename"
    sys.exit(1)

  # get parameters into correct variables
  params = (open(args[0], 'r').readline()).split()
  if len(params) > 10 or len(params) < 8:
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

  # get stimuli into an array 
  stimuli = []
  stim_file = open(args[1], 'r')

  stim_line = stim_file.readline()
  if stim_line == "":
    print "error! there must be at least one stimulus"
    sys.exit(1)
  
  while(stim_line != ""):
    stim = numpy.array([int(i) for i in stim_line.split()])
    if len(stim) != L:
      print "error! each line of stimulus file must be %d long" % L
      sys.exit(1)
    stimuli.append(stim)
    stim_line = stim_file.readline()

  stimuli = numpy.asarray(stimuli)
  
  # ---- setup of main network loop --------------
  # timing info, and message that shows it started
  start = time.clock()
  print "Starting."

  # create layers
  l4 = ldefs.L4(n4, L, k, randomize=rand, non_k=non_k)
  l23 = ldefs.L23(n23, n4, mean, stdp_eta)

  # create data structures to store info about network:
    # the number of times each neuron fired:
  l4_freqs = [0 for nrn in range(n4)]
  l23_freqs = [0 for nrn in range(n23)]
    # the spike vector in each timestep (more detailed)
  l4_out_matrix = []
  l23_out_matrix = []

  # calculate layer 4 for edge case where t = 0 (so l23_exc = 0)
    # edge case - do NOT save
  stim_0 = stimuli[0]
  l4_exc = lfuncs.excitation(l4, stim_0)
  l4_spiking_input = lfuncs.spikevec_where(lfuncs.probvec_to_spikevec(lfuncs.sig_prob(l4_exc, beta, theta)))

  # calculate layer 4 and layer 2-3 for edge case where t = 1 (l23_exc = inputWeightMatrix * L_4(t-1))
    # edge case - do NOT save
  stim_1 = stimuli[1]
  l23_exc = lfuncs.net_input_vector(l23.inputWeightMatrix, l4_spiking_input)
  l23_spiking_input = lfuncs.spikevec_where(lfuncs.probvec_to_spikevec(lfuncs.sig_prob(l23_exc, beta, theta)))

  l4_exc = lfuncs.excitation(l4, stim_1)
  l4_spiking_input = lfuncs.spikevec_where(lfuncs.probvec_to_spikevec(lfuncs.sig_prob(l4_exc, beta, theta)))


  # ---- main network loop -------------------------------
  # give the network each stimulus, updating firing rates
  for t in range(len(stimuli)):
    curr_stim = stimuli[t]

    # calculate excitation of L23 at time t = inputWeightMatrix * L4_(t-1) + recurrentWeightMatrix * L_23(t-1)
    l23_exc = lfuncs.net_input_vector(l23.inputWeightMatrix, l4_spiking_input) + lfuncs.net_input_vector(l23.recurrentWeightMatrix, l23_spiking_input)

    # turn excitation into spikes; save 
    l23_sig = lfuncs.sig_prob(l23_exc, beta, theta)
    l23_spike_vec = lfuncs.probvec_to_spikevec(l23_sig)

    l23_out_matrix.append(l23_spike_vec)

    # turn spike_vec into list of indices of neurons that spiked, update firing rates
    l23_spiking_input = lfuncs.spikevec_where(l23_spike_vec)
    for nrn in l23_spiking_input:
      l23_freqs[nrn] += 1

    # calculate excitation of L4 at time t
    l4_exc = lfuncs.excitation(l4, curr_stim)

    # turn excitation into spikes, save
    l4_sig = lfuncs.sig_prob(l4_exc, beta, theta)
    l4_spike_vec = lfuncs.probvec_to_spikevec(l4_sig)

    l4_out_matrix.append(l4_spike_vec)

    # turn spike_vec into list of indices of neurons that spiked, update firing rates
    l4_spiking_input = lfuncs.spikevec_where(l4_spike_vec)
    for nrn in l4_spiking_input:
      l4_freqs[nrn] += 1

    

    # # calculate layer 4
    # L4_exc_vec = lfuncs.excitation(l4, curr_stim)
    # L4_sig_out = lfuncs.sig_prob(L4_exc_vec, beta, theta)
    # L4_spike_vec = lfuncs.probvec_to_spikevec(L4_sig_out)
    # L4_spiking_input = lfuncs.spikevec_where(L4_spike_vec)

    # # firing rate calculation
    # for nrn in L4_spiking_input:
    #   l4_freqs[nrn]+=1


    # # calculate layer 2-3
    # L23_exc_vec = lfuncs.net_input_vector(l23.inputWeightMatrix, L4_spiking_input)
    # L23_sig_out = lfuncs.sig_prob(L23_exc_vec, beta, theta)
    # L23_spike_vec = lfuncs.probvec_to_spikevec(L23_sig_out)
    # L23_spiking_input = lfuncs.spikevec_where(L23_spike_vec)

    # # calculate layer 2-3 recurrent
    # L23r_exc_vec = lfuncs.net_input_vector(l23.recurrentWeightMatrix, L23_spiking_input)
    # L23r_sig_out = lfuncs.sig_prob(L23r_exc_vec, beta, theta)
    # L23r_spike_vec = lfuncs.probvec_to_spikevec(L23r_sig_out)

    # # firing rate calculation
    # for nrn in lfuncs.spikevec_where(L23r_spike_vec):
    #   l23_freqs[nrn] += 1
  
  # write firing rates to output files in plottable format 
  l4_out = open(args[2], 'a')
  for f in l4_freqs:
    l4_out.write("%d, " % f)
  l4_out.write('\n')
  l4_out.close()

  l23_out = open(args[3], 'a')
  for f in l23_freqs:
    l23_out.write("%d, " % f)
  l23_out.write('\n')
  l23_out.close()

  end = time.clock()
  print "Finished. Total time: %f" % (end - start)



if __name__ == "__main__":
  main()