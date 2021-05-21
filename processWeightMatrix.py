import sys
import numpy
import time

def string_to_matrix(args):
    in_file = open(args[0], 'r')
    out_file_line = in_file.readline()
    out_file_line = out_file_line.split(", ")
    out_file = open(out_file_line[0], out_file_line[1])

    st = time.clock()

    dimension_line = in_file.readline()

    while dimension_line != '':
        dimensions = dimension_line.split(", ")
        num_row = int(dimensions[0].split(": ")[1])
        num_col = int(dimensions[1].split(": ")[1])

        weight_string = in_file.readline()
        if weight_string == '':
            print("Error! Insufficient number of weight matrices.")

        weight_list = weight_string.split(",")
        
        for row in range(num_row):
            start = row * num_col
            end = start + num_col
            out_file.write(",".join(weight_list[start:end]) + '\n')

        dimension_line = in_file.readline()

    et = time.clock()
    print("Time: %f" % (et - st))
    
def single_matrix(matrix_filename, rows, cols, out_filename, mode='a'):
    matrix_string = open(matrix_filename, 'r').readline()
    matrix_list = matrix_string.split(",")

    out_file = open(out_filename, mode)

    for r in range(rows):
        start = r * cols
        end = start + cols
        out_file.write(",".join(matrix_list[start:end]) + '\n')

    out_file.close()

def main():
    """ processes weight matrix produced using tofile ()
        turns into separate lines for each row of the weight matrix
        separated by commas
        default use:
        input file format should be:
        line 1: out_filename, mode (a or w)
        line 2: number of rows: (number), number of columns: (number) 
        line 3: entire weight matrix as string separated by commas
        line 4-5 on: can repeat 2 and 3 
        if -single is first argument will use command line arguments:
            -single weight_matrix_filename rows columns output_filename [mode]

        example:
        test_out.txt, a
        number of rows: 3, number of columns: 2
        1,2,3,4,5,6
        number of rows: 2, number of columns: 3
        1,2,3,4,5,6

        outputs:
        1,2
        3,4
        5,6

        1,2,3
        4,5,6
    """
    # get input
    args = sys.argv[1:]
    if args[0] == "-single":
        mode = 'a'
        if len(args) == 6:
            mode = 'w'
        single_matrix(args[1], int(args[2]), int(args[3]), args[4], mode=mode)
    else:
        string_to_matrix(args)

if __name__ == "__main__":
  main()