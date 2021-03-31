import sys
import numpy

def main():
    """ arguments: input_filename, output_filename number of stimuli in each line (L)
        prints frequency of each stimulus and correlation matrix
        writes correlation matrix to output_filename in comma separated format
    """
    args = sys.argv[1:]
    input_filename = args[0]
    output_filename = args[1]
    L = int(args[2])
    
    f = open(input_filename, 'r')

    # total occurences of each stimulus; list of length L
    stim_freq = [0 for i in range(L)]
    # frequency of i appearing after j; L x L matrix
    corr = numpy.zeros((L, L), dtype=int)

    line = f.readline()
    prev_stim = -1

    while(line != ''):
        line = line.split()

        for i in range(L):
            # find current stimulus
            if int(line[i]) == 1:
                # update stim_freq
                stim_freq[i] += 1

                # update correlation matrix
                if prev_stim != -1:
                    corr[prev_stim][i] += 1
                prev_stim = i

                break # no need to iterate over zeroes

        line = f.readline()
    
    print "Stimulus frequency:\n" + str(stim_freq)
    print "Correlation matrix:\n" + str(corr)

    out = open(output_filename, 'a')
    for prev in range(L):
        out.write("prev = %d, " % prev)
        for curr in range(L):
            out.write("%d, " % corr[prev][curr] )
        out.write("\n")
    out.close()


if __name__ == "__main__":
  main()