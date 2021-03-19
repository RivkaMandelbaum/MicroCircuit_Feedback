import os
import re
import sys
import random

def main():
    """ appends to file with name output_filename, 
    n repetitions of each of the vec[1-9].txt files in 
    input-files folder, in
    random order. 
    """
    args = sys.argv[1:]
    if not args or len(args) != 2:
        print "usage: output_filename n"
        sys.exit(1)

    output_filename = args[0]
    n = int(args[1])
    
    filenames = os.listdir("input-files")
    vecs = []

    for f in filenames:
        match = re.search("vec[1-9]\.txt", f)
        if match:
            fullname = "input-files/" + match.group()
            stim_vec = open(fullname, 'r').readline()
            vecs.append(stim_vec)

    out = open(output_filename, 'a')
    
    end = len(vecs)-1
    for i in range(n):
        vec_index = random.randint(0, end)
        out.write(vecs[vec_index])

    out.close()


if __name__ == "__main__":
  main()