
import sys
import numpy  
import random
import math 

# a basic implementation of layer 4 
class L4:
  """ L4 objects represent layer 4 in the cortex. Layers have n4 neurons, L stimuli, (if initialized from scratch) k neurons initially given activation, and a weightMatrix, an n4 x L numpy array. """

  def __init__(self, n4, L, k, randomize=False, non_k=-1, given_weight_matrix = None):
    """ Initialize layer 4 object with n4 neurons, L stimuli, k neurons with initial activation (unless given_weight_matrix provided), and weightMatrix.
    If given_weight_matrix is provided (not None), it must either be in the form of a string containing n4*L values separated by commas, or in the form of a numpy array of the correct dimensions. The layer's weightMatrix is initialized with values matching given_weight_matrix. 
    If given_weight_matrix is not provided, k neurons per stimuli are chosen to have activation of +1. If randomize=True, these are chosen randomly, otherwise the first k neurons respond to the first stimulus and so on. The remaining neurons are filled with non_k (-1 by default). 
    """

    self.n4 = n4
    self.L = L
    self.k = k
    self.weightMatrix = numpy.full((self.n4, self.L), non_k, dtype=numpy.int16)

    # initializing from the start
    if given_weight_matrix == None: 
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

    # initializing from previous weight matrix, given as string or as prepared weight matrix
    else: 
      if type(given_weight_matrix) is str:
        l4_weight_list = [int(i) for i in given_weight_matrix.split(",")]
        
        if len(l4_weight_list) != (self.n4 * self.L):
          print("Error! String provided to initialize L4 weight matrix must have length n4 * L.")
          sys.exit(1)

        for nrn in range(self.n4):
          start = nrn * self.L 
          end = start + self.L
          self.weightMatrix[nrn] = numpy.array(l4_weight_list[start:end])
      else:
        if given_weight_matrix.shape != (n4, L):
          print("Error! Matrix provided to initialize L4 weight matrix must have shape (n4, L)")
          sys.exit(1)
        self.weightMatrix = given_weight_matrix
      

class L23: 
  """ L23 objects represent layers 2 and 3 in the cortex. Layers have n23 neurons and are connected to n4 neurons in layer 4. Layers have an inputWeightMatrix, representing connection from layer 4 to layer 2/3, which is a (n23, n4) numpy array, and a recurrentWeightMatrix, representing recurrent connections, which is a (n23, n23) numpy array."""

  def __init__(self, n23, n4, mean, stdp_eta, given_weight_matrices = None):
    """ Initializes a layer 2/3 object with n23 neurons connected to n4 neurons from layer 4. 
    If initialized from scratch, creates (n23, n4) inputWeightMatrix with weights chosen by Gaussian distribution with mean provided and stdv = 1/sqrt(n4), and (n23, n23) recurrentWeightMatrix with weights chosen by Gaussian with stdv = 1/sqrt(n4) and diagonal filled with zeroes.
    If given_weight_matrices provided, it should be a list with two matrices, input and recurrent, either as (n23 * n4)-length or (n23 * n23)-length strings, or as (n23, n4) or (n23, n23) matrices. 
    """
    self.n23 = n23
    self.n4 = n4
    self.eta = stdp_eta

    # initialize from scratch
    if given_weight_matrices == None:
      # create input weight matrix with weights chosen by Gaussian distribution
      stdv = 1/math.sqrt(n4)
      self.inputWeightMatrix = numpy.random.normal(mean, stdv, (n23, n4))

      # create recurrent weight matrix, set diagonal to zero
      stdv = 1/math.sqrt(n23)
      self.recurrentWeightMatrix = numpy.random.normal(mean, stdv, (n23, n23))
      numpy.fill_diagonal(self.recurrentWeightMatrix, 0)
    
    # initialize from given weight matrices (should be a tuple with two elements)
    else:
      if len(given_weight_matrices) != 2:
        print("Error: kwarg given_weight_matrices in initializion of L23 object must be a tuple of (inputWeighMatrix, recurrentWeightMatrix)")
        sys.exit(1)

      self.inputWeightMatrix = numpy.zeros((self.n23, self.n4))
      self.recurrentWeightMatrix = numpy.zeros((self.n23, self.n23))
      
      # input weight matrix: 
      # given as string
      if type(given_weight_matrices[0]) is str:
        l23_weight_list = [float(i) for i in given_weight_matrices[0].split(",")]
        if len(l23_weight_list) != (self.n23 * self.n4):
          print("Error! String provided to initialize L23 input weight matrix must have length n23 * n4.")
          sys.exit(1)

        for nrn in range(self.n23):
          start = nrn * self.n4 
          end = start + self.n4
          self.inputWeightMatrix[nrn] = numpy.array(l23_weight_list[start:end])
      # given as complete matrix
      else:
        if given_weight_matrices[0].shape != (self.n23, self.n4):
          print("Error! Matrix provided to initialize L23 input weight matrix must have shape (n23, n4)")
          sys.exit(1)

        self.inputWeightMatrix = given_weight_matrices[0]

      #recurrent weight matrix:
      # given as string
      if type(given_weight_matrices[1]) is str:
        l23_weight_list = [float(i) for i in given_weight_matrices[1].split(",")]
        if len(l23_weight_list) != (self.n23 * self.n23):
          print("Error! String provided to initialize L23 recurrent weight matrix must have length n23 * n23.")
          sys.exit(1)
        for nrn in range(self.n23):
          start = nrn * self.n23
          end = start + self.n23
          self.recurrentWeightMatrix[nrn] = numpy.array(l23_weight_list[start:end])
      # given as complete matrix
      else:
        if given_weight_matrices[1].shape != (self.n23, self.n23):
          print("Error! Matrix provided to initialize L23 recurrent weight matrix must have shape (n23, n23)")
          sys.exit(1) 

        self.recurrentWeightMatrix = given_weight_matrices[1]


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
