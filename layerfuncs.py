# contains functions that deal with input and output of layers
import numpy
import matplotlib.pyplot as plt

# import layerdefs as ldefs

def excitation(layer, input):
    """ given a layer and an input vector, return the output vector
    of neuron excitation, before applying nonlinearity or thresholds to the spikes
    """
    return numpy.dot(layer.weightMatrix, input) 

def sig_prob(excit_vec, beta, theta):
    """ given an excitation vector, and parameters beta (constant)and theta (threshold) for sig function, return the probability vector representing probability of firing for each neuron in the vector
    """
    excit_transform = -beta * (excit_vec - theta) # operators work elementwise
    excit_exp = numpy.exp(excit_transform)

    return 1/(1 + excit_exp)

def probvec_to_spikevec(probvec):
    """ given a vector representing probability of firing for each neuron in the layer, use probability to choose whether each neuron does fire
    """
    spikevec = []

    for i in range(len(probvec)): 
        p_tuple = (1-probvec[i], probvec[i])
        choice = int(numpy.random.choice((0, 1), p=p_tuple))
        spikevec.append(choice)

    return spikevec    

def spikevec_toString(spikevec):
    """ given a vector representing which neurons spiked, returns a string
    of indices of neurons whose values were 1 
    """
    string_out = ""
    for nrn in range(len(spikevec)):
        if spikevec[nrn] == 1:
            string_out += (" " + str(nrn))
    return string_out

def spikevec_where(spikevec):
    """ given a vector representing which neurons spiked, returns an array
    containing indices of neurons whose values were 1 in the vector 
    """
    arr = []
    for nrn in range(len(spikevec)):
        if (spikevec[nrn] == 1):
            arr.append(nrn)
    return arr

def net_input(weight_matrix, neuron, spiking_input):
    """ given a weight matrix and a neuron, returns
    the  sum of all weights of inputs to that neuron which are spiking,
    as indicated by their indices in spiking_input. 
    That is, for an m x n matrix with rows i
    and columns j, given a row i returns the sum of all
    weights j of spiking neurons, representing voltage into neuron i
    """
    sum = 0
    for j in spiking_input:
        sum += weight_matrix[neuron][j]
    return sum

def net_input_vector(weight_matrix, spiking_input):
    """ given a weight_matrix and indices of spiking neurons
    in input,  returns array of sum of weights of inputs to
    each neuron. That is, for mxn matrix with rows
    i and columns j, returns an m x 1 vector of
    sums of all columns j for each i. Uses net_input 
    function. Returns numpy array. 
    """
    m = len(weight_matrix)
    result_vec = [net_input(weight_matrix, i, spiking_input) for i in range(m)]
    return numpy.array(result_vec)