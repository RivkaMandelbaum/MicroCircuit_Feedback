# a basic implementation of layer 4 

import sys
import numpy  
import random

# define class L4
class L4:
  # number of inputs 
  L = 9
  firePerStim = 4  

  # init L4 object with n4 neurons, create and initialize weight matrix 
  def __init__(self, n4):
    self.n4 = n4
    self.weightMatrix = numpy.zeros((n4, self.L), dtype=numpy.int16)

    #initialize weight matrix: for each stimulus, pick four neurons that respond 
    for i in range(self.L):
      # list of which will respond
      responds = random.sample(range(n4), k=self.firePerStim)
      # update weightMatrix
      for j in responds: 
        self.weightMatrix[j][i] = 1

  def always_fire(self, input):
    return self.weightMatrix.dot(input) 

  def sigmoid_fire(self, input):
    # make p_fire array of probabilities that each neuron will fire 
    always_out = self.always_fire(input)
    p_fire = 1/(1+ numpy.exp(always_out))

    # use probability of firing to choose whether it fires
    #sig_out = [int(numpy.random.choice((0,1), 1, [1-p_fire[i], p_fire[i]])) for i in range(self.n4)]
    sig_out = []
    for i in range(self.n4):
      if always_out[i] == 1:
        sig_out.append(int(numpy.random.choice((0,1), 1, [1-p_fire[i], p_fire[i]])))
      else: 
        sig_out.append(0)   
    return sig_out

  def fire_out_toString(self, fire_out):
    string_out = ""
    for nrn in self.fire_out_where(fire_out):
      string_out += (" " + str(nrn))
    return string_out

  def fire_out_where(self, fire_out):
    arr = []
    for nrn in range(self.n4):
      if (fire_out[nrn]):
        arr.append(nrn)
    
    return arr

def main():
  """ reads n4 (number of neurons in layer 4, int) and input_filename (string) from command line, creates an L4 object and returns an output vector of neurons that fired. input file format: 1's (for stimuli present) or 0's separated by single whitespace character """
  # get command line arguments into args array
  args = sys.argv[1:] 
  if not args or len(args) != 2: 
    print "usage: number_of_neurons input_filename"
    sys.exit(1) 
  
  # get n4 and instantiate an L4 object  
  n4 = int(args[0])
  l4 = L4(n4)

  # using filename from input, create input vector
  # opens, reads as one string, splits on whitespace, converts each to int
  input_filename = args[1]
  input = numpy.array([int(i) for i in ((open(input_filename, 'r')).read()).split()])
  if len(input) != l4.L:
    print "error: there must be %d stimuli" % l4.L
    sys.exit(1)

  # print an output vector of neurons that fired
  print "Assuming neurons always fire: " + l4.fire_out_toString(l4.always_fire(input))
  print "Feeding through sigmoid: " + l4.fire_out_toString(l4.sigmoid_fire(input))

  
  



if __name__ == "__main__":
  main()