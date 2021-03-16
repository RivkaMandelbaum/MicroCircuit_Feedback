import os 
import re
import sys

def main():
    """ appends the text in usage_string_filename to all files in
        directory whose name matches in[0-9]+.*txt
    """
    args = sys.argv[1:]
    if not args or len(args) > 2:
        print "usage: usage_string_filename directory"
        sys.exit(1)
    
    usage_string_file = args[0]
    directory = sys.argv[1]

    usage_string = (open(usage_string_file, 'r')).read()
    
    for filename in os.listdir(directory):
        if re.search("in[0-9]+.*txt", filename) is not None: 
            path = directory + "/" + filename
            file = open(path, 'a')
            file.write(usage_string)
            print "modified " + path
            file.close()

if __name__ == "__main__":
  main()