import os
import re
import sys
import random
from datetime import datetime

def write_random(out, n, vecs):
    end = len(vecs)-1
    for i in range(n):
        vec_index = random.randint(0, end)
        out.write(vecs[vec_index])

def write_seq(out, vecs, linesToPrint):
    seq_start = random.choice([0,3,6])

    for i in range(linesToPrint):
        out.write(vecs[seq_start+i])

def create_output_filename(hmm, n):
    # creates output filename in format: 
        # rand-number_of_lines-date.txt, or, 
        # hmm-number_of_lines-date.txt
    output_filename = "input-files/stims/TEST-"
    if hmm:
        output_filename += "hmm-"
    else:
        output_filename += "rand-"
    
    # number of lines
    output_filename += n

    # date
    today = datetime.today()
    month = str(today.month)
    day = str(today.day)

    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day

    datestring = month+day    
    output_filename += ("-" + datestring + ".txt")

    if(os.path.exists(output_filename)):
        change = input("A file with this name already exists! Do you want to overwrite (if no, will add -HHMM-SS)? [y/n]")
        if change == "n":
            now = datetime.now()
            hour = str(now.hour)
            minute = str(now.minute)
            second = str(now.second)

            timestring = "-" + hour + minute + "-" + second

            output_filename = output_filename[:-4]
            output_filename += timestring + ".txt"
        elif change != "y":
            print("Error! Must respond with 'y' or 'n'.")
            sys.exit(1)

    return output_filename


def main():
    """ creates n lines of input to the network, where each line of 
    input is one of the vec[1-9].txt files in input-files/vecs. The
    input is in random order if -random specified, and contains sequences
    mixed with noise if -hmm is specified. 
    By default, the program creates a file in input-files/stims named: 
    (rand/hmm)-(number of lines)-(MMDD).txt and places output there. 
    Access mode and output filename can be specified on the command line, e.g.
    python3 generateInput.py 100 -random -w existingfile.txt would overwrite
    existing file with 100 random stimuli. 
    """
    # get arguments
    args = sys.argv[1:]
    if not args or len(args) == 3 or len(args) > 4:
        print("usage: n (-random or -hmm) [-mode filename]")
        sys.exit(1)

    n = int(args[0])
    hmm = True

    if args[1] == "-random":
        hmm = False
    elif args[1] != "-hmm":
        print("Error! Second argument must be -random or -hmm.")
        sys.exit(1)

    mode = 'w+'
    if len(args) == 4: 
        mode_flag = args[2]
        mode = mode_flag[1:]
        output_filename = args[3]
    else:
        # filename format is: rand/hmm-number_of_lines-date.txt 
        output_filename = create_output_filename(hmm, str(n))



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
    out = open(output_filename, mode=mode)

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