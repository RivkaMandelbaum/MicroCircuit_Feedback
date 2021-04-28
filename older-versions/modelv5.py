import sys
import time
import numpy
import layerdefs as ldefs
import layerfuncs as lfuncs
import os

def main():
  """ reads filename and flags from command line. The file named should contain:
        Line 1: input parameters, described in "usage" sections of input files. 
        Line 2: stim_filename: the file should contain stimulus vectors, one on each line. (minimum one stimulus). 
        Line 3: l4_output_filename: will put l4 firing rates in this file. 
        Line 4:l23_output_filename: will put l23 firing rates in this file. 
        Line 5: [if -m flag specified] file with weight matrices
        Line 6: [if -s flag specified] file to save weight matrices into
      The flags available are: -m (use weight matrices from file to initialize layers), -s (save weight matrices to file at the end), and -w (overwrite output files, rather than appending). 

      creates L4 and L23 objects; calculates the firing rates in response to the stimuli given. each stimulus defines a separate timebin. 
  """

  # -------- input ------------------------
  # get command line arguments into args array
  args = sys.argv[1:] 
  if not args or len(args) > 4:
    print "usage: param_filename [-m] [s] [-w]"
    sys.exit(1)
  
  param_file = open(args[0], 'r')
  del args[0]

  # get parameters into correct variables
  params = (param_file.readline()).split()
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
  stim_file = open((param_file.readline()).rstrip('\n'), 'r')

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

  # save other parameter names (matrices_file and/or save_file)
  mode = 'a'
  flag_s = False
  flag_m = False

  for i in range(1, len(args)):
    if args[i] == "-w":
      mode = 'w'
      del args[i]
      break
      
  l4_out = open((param_file.readline()).rstrip('\n'), mode)
  l23_out = open((param_file.readline()).rstrip('\n'), mode)

  # if there are flags (remaining elements in args array), save information as needed
  if len(args) > 0:
    # one flag
    if len(args) == 1:
      if args[0] == "-m":
        matrices_file = open((param_file.readline()).rstrip('\n'), 'r')
        flag_m = True
      elif args[0] == "-s":
        save_file = open((param_file.readline()).rstrip('\n'), mode)
        flag_s = True
      else:
        print "Only -s, -m, and -w are valid flags"
        sys.exit(1)
    # two flags
    elif len(args) == 2: 
      # -m first
      if args[0] == "-m":
        matrices_file = open((param_file.readline()).rstrip('\n'), 'r')
        flag_m = True
        if args[1] == "-s":
          save_file = open((param_file.readline()).rstrip('\n'), mode)
          flag_s = True
        else:
          print "Only -s, -m, and -w are valid flags"
          sys.exit(1)
      # -s first
      elif args[0] == "-s":
        save_file = open((param_file.readline()).rstrip('\n'), mode)
        flag_s = True
        if args[1] == "-m":
          matrices_file = open((param_file.readline()).rstrip('\n'), 'r')
          flag_m = True
        else:
          print "Only -s, -m, and -w are valid flags"
          sys.exit(1)
      # error
      else:
        print "Only -s, -m, and -w are valid flags"
        sys.exit(1)

  # ---- setup of main network loop --------------
  # timing info, and message that shows it started
  start_time = time.clock()
  print "Starting."

  # create layers
  if flag_m:
    l4_weight_string = matrices_file.readline()
    l23_input_string = matrices_file.readline()
    l23_recurrent_string = matrices_file.readline()

    l4 = ldefs.L4(n4, L, k, randomize=rand, non_k=non_k, given_weight_matrix=l4_weight_string)

    l23 = ldefs.L23(n23, n4, mean, stdp_eta, given_weight_matrices=(l23_input_string, l23_recurrent_string))

  else:
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
    # edge case - do NOT save in freqs
  stim_0 = stimuli[0]
  l4_exc = lfuncs.excitation(l4, stim_0)
  l4_spike_vec = lfuncs.probvec_to_spikevec(lfuncs.sig_prob(l4_exc, beta, theta))
  l4_spiking_input = lfuncs.spikevec_where(l4_spike_vec)

  l4_out_matrix.append(l4_spike_vec)
  l23_out_matrix.append([0 for nrn in range(n23)])

  # calculate layer 4 and layer 2-3 for edge case where t = 1 (l23_exc = inputWeightMatrix * L_4(t-1))
    # edge case - do NOT save in freqs
  stim_1 = stimuli[1]
  l23_exc = lfuncs.net_input_vector(l23.inputWeightMatrix, l4_spiking_input)
  l23_spike_vec = lfuncs.probvec_to_spikevec(lfuncs.sig_prob(l23_exc, beta, theta))
  l23_spiking_input = lfuncs.spikevec_where(l23_spike_vec)

  l23_out_matrix.append(l23_spike_vec)

  l4_exc = lfuncs.excitation(l4, stim_1)
  l4_spike_vec = lfuncs.probvec_to_spikevec(lfuncs.sig_prob(l4_exc, beta, theta))
  l4_spiking_input = lfuncs.spikevec_where(l4_spike_vec)

  l4_out_matrix.append(l4_spike_vec)

  # ---- main network loop -------------------------------
  # give the network each stimulus, updating firing rates
  for t in range(2, len(stimuli)):
    curr_stim = stimuli[t]

    # calculate excitation of L23 at time t = inputWeightMatrix * L4_(t-1) + recurrentWeightMatrix * L_23(t-1)
    l23_exc = lfuncs.net_input_vector(l23.inputWeightMatrix, l4_spiking_input) + lfuncs.net_input_vector(l23.recurrentWeightMatrix, l23_spiking_input)

    # turn excitation into spikes
    l23_sig = lfuncs.sig_prob(l23_exc, beta, theta)
    l23_spike_vec = lfuncs.probvec_to_spikevec(l23_sig)

    # save spikes and firing rates
    l23_out_matrix.append(l23_spike_vec)

    prev_l23_spiking_input = l23_spiking_input
    l23_spiking_input = lfuncs.spikevec_where(l23_spike_vec)

    for nrn in l23_spiking_input:
      l23_freqs[nrn] += 1

    # use saved spikes and current spikes to implement stdp rule:
    # synapse k>k' is represented by l23.recurrentWeightMatrix[k'][k]
    # for k>k', if k spiked in t-1 and k' spiked in t, increase weight by eta
    # if k spiked in t and k' in t-1, decrease weight by eta
    for curr_spike in l23_spiking_input: 
      for prev_spike in prev_l23_spiking_input:
        l23.recurrentWeightMatrix[curr_spike][prev_spike] += l23.eta
        l23.recurrentWeightMatrix[prev_spike][curr_spike] -= l23.eta

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
  
  # write firing rates to output files in plottable format 
  for f in l4_freqs:
    l4_out.write("%d, " % f)
  l4_out.write('\n')
  for line in l4_out_matrix:
    l4_out.write(', '.join(map(str,line)))
    l4_out.write('\n')
  l4_out.close()

  for f in l23_freqs:
    l23_out.write("%d, " % f)
  l23_out.write('\n')
  for line in l23_out_matrix:
    l23_out.write(', '.join(map(str,line)))
    l23_out.write('\n')
  l23_out.close()

  # save weight matrices to file if -s flag specified
  if flag_s: 
    (l4.weightMatrix).tofile(save_file, sep= ",", format = "%s")
    save_file.write('\n')
    (l23.inputWeightMatrix).tofile(save_file, sep= ",", format = "%s")
    save_file.write('\n')
    (l23.recurrentWeightMatrix).tofile(save_file, sep= ",", format = "%s")

  end_time = time.clock()
  print "Finished. Total time: %f" % (end_time - start_time)



if __name__ == "__main__":
  main()