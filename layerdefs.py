
import sys
import numpy  
import random
import math 

# a basic implementation of layer 4 
class L4:
  # initialize L4 object with n4 neurons, L stimuli, k neurons initially given activation +1 per stimuli
  # weightMatrix is initialized to have -1 activation for all but the k neurons per stimulus by default, but can change non_k
  # the neurons are chosen randomly if randomize = True, but by default the first k neurons respond to the first stimulus and so on
  def __init__(self, n4, L, k, randomize=False, non_k=-1):
    self.n4 = n4
    self.L = L
    self.k = k
    self.weightMatrix = numpy.full((n4, self.L), non_k, dtype=numpy.int16)

    if randomize == "True":
      #initialize weight matrix: for each stimulus, pick k neurons that respond randomly
      for stim in range(self.L):
        # randomly samples k neurons to respond (out of n4)
        responds = random.sample(range(n4), k=self.k)
        # updates the values of those k neurons' responses to stimulus 
        for nrn in responds: 
          self.weightMatrix[nrn][stim] = 1
    else:
      start_nrn = 0
      # the first k neurons respond to first stimulus, and so on
      for stim in range(self.L):
        for nrn_offset in range(self.k):
          self.weightMatrix[start_nrn + nrn_offset][stim] = 1
        start_nrn += self.k



class L23: 
  def __init__(self, n23, n4, mean, stdp_eta):
    self.n23 = n23
    self.n4 = n4

    stdv = 1/math.sqrt(n4)
    self.inputWeightMatrix = numpy.random.normal(mean, stdv, (n23, n4))

    stdv = 1/math.sqrt(n23)
    self.recurrentWeightMatrix = numpy.random.normal(mean, stdv, (n23, n23))
    print self.inputWeightMatrix
    print self.recurrentWeightMatrix


# # a basic implementation of layer 6 
# class L6:
#   # initialize L6 object with n6 neurons, receiving input from n23 neurons, with k neurons initially given activation +1 per input
#   # weightMatrix is initialized to have -1 activation for all but the k neurons per stimulus by default, but can change non_k
#   # the neurons are chosen randomly if randomize = True, but by default the first k neurons respond to the first stimulus and so on
#   def __init__(self, n6, n23, k, randomize=False, non_k=-1):
#     self.n6 = n6
#     self.n23 = n23
#     self.k = k
#     self.weightMatrix = numpy.full((n6, n23), non_k, dtype=numpy.int16)

#     if randomize == "True":
#       #initialize weight matrix: for each stimulus, pick k neurons that respond randomly
#       for stim in range(n23):
#         # randomly samples k neurons to respond (out of n6)
#         responds = random.sample(range(n6), k=self.k)
#         # updates the values of those k neurons' responses to stimulus 
#         for nrn in responds: 
#           self.weightMatrix[nrn][stim] = 1
#     else:
#       start_nrn = 0
#       # the first k neurons respond to first stimulus, and so on
#       for stim in range(n23):
#         for nrn_offset in range(self.k):
#           self.weightMatrix[start_nrn + nrn_offset][stim] = 1
#         start_nrn += self.k
