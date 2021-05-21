import sys
import numpy as np
import matplotlib.pyplot as plt

def main(): 
    """ arguments: prefile name, postfile name
        (files should contain the line of output of running calculateFiringRates.py with -index created after "Tuning indices:")
        if scatter desired: xlabel, ylabel for scatter
        if ylim desired: bottom, top
    """
    args = sys.argv[1:]
    prestring = open(args[0], 'r').readline()
    poststring = open(args[1], 'r').readline()

    pre = np.asarray([float(i) for i in prestring[1:-2].split(', ')])
    post = np.asarray([float(i) for i in poststring[1:-2].split(', ')])

    plt.hist(pre, histtype="step", label="pre")
    plt.legend()
    plt.savefig('%s-hist.png' % (args[0]))
    plt.show()

    plt.hist(post, histtype="step", label="post")
    plt.legend()
    plt.savefig('%s-hist.png' % (args[1]))
    plt.show()


    plt.hist(pre, histtype="step", label="pre")
    plt.hist(post, histtype="step", label="post")
    plt.legend()
    plt.savefig('%s-%s-hist.png' % (args[0], args[1]))
    plt.show()

    if len(args) > 2:
        plt.scatter(pre, post)
        if len(args) > 4:
            plt.ylim(float(args[4]), float(args[5]))
        plt.xlabel(args[2])
        plt.ylabel(args[3])
        plt.savefig('%s-%s-scatter.png' % (args[0], args[1]))
        plt.show()


    
if __name__ == "__main__":
  main()