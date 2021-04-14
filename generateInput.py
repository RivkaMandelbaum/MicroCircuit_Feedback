import os
import re
import sys
import random

def write_random(out, n, vecs):
    end = len(vecs)-1
    for i in range(n):
        vec_index = random.randint(0, end)
        out.write(vecs[vec_index])

def write_seq(out, vecs, linesToPrint):
    seq_start = random.choice([0,3,6])

    for i in range(linesToPrint):
        out.write(vecs[seq_start+i])


def main():
    """ appends to file with name output_filename, 
    n repetitions of each of the vec[1-9].txt files in 
    input-files/vecs folder, in random order if --random order
    or using hidden markov model to generate sequences mixed with noise. 
    """
    # get arguments
    args = sys.argv[1:]
    if not args or len(args) > 3:
        print "usage: output_filename n [--random]"
        sys.exit(1)

    output_filename = args[0]
    n = int(args[1])
    hmm = True
    if len(args) == 3:
        if args[2] == "--random":
            hmm = False
        else:
            print "final argument should be -random flag"
            sys.exit(1)

    # create list of vectors (stimuli to print to file)
    filenames = os.listdir("input-files/vecs")
    vecs = []
    vecnames = []

    for f in filenames:
        match = re.search("vec[1-9]\.txt", f)
        if match:
            fullname = "input-files/vecs/" + match.group()
            vecnames.append(fullname)
    
    vecnames.sort()
    
    for v in vecnames:
        stim_vec = open(v, 'r').readline()
        vecs.append(stim_vec)
    
    # write to file
    out = open(output_filename, 'a')

    # if "-random" provided, write n random stimuli
    if not hmm: 
        write_random(out, n, vecs)
    # otherwise write using hidden markov model with temporal sequences
    else: 
        t = 0
        while t < n:
            isSequence = random.choice([True, False, False, False])
            if isSequence:
                linesLeft = n - t
                if linesLeft > 3:
                    linesLeft = 3

                write_seq(out, vecs, linesLeft)
                t += linesLeft 
            else:
                write_random(out, 1, vecs)
                t += 1


    out.close()



if __name__ == "__main__":
  main()