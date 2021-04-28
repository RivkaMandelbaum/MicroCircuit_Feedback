import matplotlib.pyplot as plt
import numpy as np
import sys


def plot_firing_rates(freqs, plot_name, layer_type):
  plt.hist(freqs)
  rm_dir_name = plot_name.split('/')[-1] # remove directories
  base_name = rm_dir_name.split('.')[0] # remove extension

  plt.title("%s firing rates: %s" % (layer_type, base_name))
  plt.xlabel("# of times fired")
  plt.savefig(plot_name)
  plt.close()

def plot_firing_rate_changes(plot_name, pre_freqs, post_freqs=None, input_type="array", layer_label=None):
  """ creates 1 or 2 plots of firing rates: 
      1. histogram of pre_freqs (if post_freqs specified, will plot histogram of post_freqs on same figure)
      2. if post_freqs specified: scatterplot of pre_freqs against post_freqs
    input_type can be 'array' (default) or 'file', in which case pre_freqs and post_freqs should be complete filenames. 
    layer_label is used for the plot title. 
    Saves to file(s): 'plots/plot-name-[hist/scatter].png' where plot-name is the plot_name parameter without directories or extensions""" 
  
  # create base name (no directories or extensions) 
  base_name = plot_name.split('/')[-1]
  base_name = base_name.split('.')[0]

  # turn files into arrays (if input_type is 'file')
  if input_type == "file":
    pre_filename = pre_freqs
    post_filename = post_freqs

    # pre_string = ((open(pre_filename)).readline()).rstrip('\n')
    # print(pre_string)
    pre_string = ((open(pre_filename)).readline()).rstrip('\n')
    pre_freqs = [int(i) for i in pre_string.split(', ') if i]

    if post_freqs != None:
      post_string = ((open(post_filename)).readline()).rstrip('\n')
      post_freqs = [int(i) for i in post_string.split(', ') if i]
  elif input_type != "array":
    print("Error! Invalid input_type to plot firing rate changes!")
    sys.exit(1)

  # plot histograms
  if post_freqs != None:
    pre_label = "pre"
    post_label = "post"
    if input_type == "file":
      pre_label += ": " + pre_filename.split('/')[-1]
      post_label += ": " + post_filename.split('/')[-1]
    plt.hist(pre_freqs, label=pre_label, alpha=0.5)
    plt.hist(post_freqs, label=post_label, alpha=0.5)
    plt.legend()
  else:
    plt.hist(pre_freqs)
  plt.title("%s firing rates: %s" % (layer_label, base_name))
  plt.xlabel("# of times fired")
  plt.savefig("plots/" + base_name + "-hist.png")
  plt.close()

  # plot scatterplot if relevant
  if post_freqs != None:
    plt.scatter(pre_freqs, post_freqs)
    
    xlabel = "Firing rates in pre-freqs"
    ylabel = "Firing rates in post-freqs"
    if input_type == "file":
      xlabel += ": " + pre_filename.split('/')[-1]
      ylabel += ": " + post_filename.split('/')[-1]
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title("%s firing rates: %s" % (layer_label, base_name))
    plt.savefig("plots/" + base_name + "-scatter.png")
    plt.close()

def plot_weight_changes(plot_name, l23_input_string, l23_recurrent_string, l23):
  """ creates four plots: 
    1. histograms of input string ("pre") and l23.inputWeightMatrix ("post")
    2. histograms of recurrent string ("pre") and l23.recurrentWeightMatrix ("post")
    3. scatterplot of input string against l23.inputWeightMatrix
    4. scatterplot of recurrent string against l23.recurrentWeightMatrix
  saves to files: plots/plot_name-[hist/scatter]-compare-pre-post-[input/rec].png
  """
  # strip directories and extensions (if any) from plot_name
  base_name = plot_name.split('.')[0]
  base_name = base_name.split('/')[-1]

  # turn strings into numpy arrays
  prev_input_list = [float(i) for i in l23_input_string.split(",")]
  prev_rec_list= [float(i) for i in l23_recurrent_string.split(",")]

  prev_input = np.asarray(prev_input_list)
  prev_rec = np.asarray(prev_rec_list)
  
  # turn weight matrices into 1D numpy arrays
  post_input = (l23.inputWeightMatrix).flatten()
  post_rec = (l23.recurrentWeightMatrix).flatten()

  # plot (input - serves as a check, since it should be the same pre/post)
  plt.hist(prev_input, alpha=0.5, label="pre")
  plt.hist(post_input, alpha=0.5, label="pre")
  plt.legend()

  plt.title("Distribution of weights, input matrix, in first file vs. second file.\n %s" % base_name)

  plt.savefig("plots/" + base_name + "-hist-compare-pre-post-input.png")
  plt.close()

    # scatterplot of input
  plt.scatter(prev_input, post_input)

  plt.title("Distribution of weights, input matrix, in first file vs. second file.\n %s" % base_name)

  plt.savefig("plots/" + base_name + "-scatter-compare-pre-post-input.png")
  plt.close()

  # plot (recurrent - with stdp on, should be different pre/post)
  plt.hist(prev_rec, alpha=0.5, label="pre")
  plt.hist(post_rec, alpha=0.5, label="post")
  plt.legend()

  plt.title("Distribution of weights, recurrent matrix, in first file vs. second file.\n %s" % base_name)

  plt.savefig("plots/" + base_name + "-hist-compare-pre-post-rec.png")
  plt.close()

      # scatterplot of rec
  plt.scatter(prev_rec, post_rec)

  plt.title("Distribution of weights, recurrent matrix, in first file vs. second file.\n %s" % base_name)

  plt.savefig("plots/" + base_name + "-scatter-compare-pre-post-rec.png")
  plt.close()

def weights(layer=None):
  # reads a single weight matrix filename saved by the model using tofile
  # plots a histogram of weights
  # assuming that the filenames are generated by ~/bin/autonet 
  if layer != None and layer != "-layer4" and layer != "-in23":
    print("invalid flag!")
    sys.exit(1)

  f = input("weight matrix filename (no directories), or 'done': ")

  while f != "done":
    f = "output-files/saved_weights/" + f

    # read from file
    wm_file = open(f)

    wm_str = wm_file.readline() #read layer 4 weightss
    if layer != "-layer4":
      wm_str = wm_file.readline() #read input layer2-3 weights
      if layer != "-in23":
        wm_str = wm_file.readline() #read recurrent weights

    wm = [float(i) for i in wm_str.split(',')]
    wm = np.asarray(wm)

    # plot
    plt.hist(wm)

    # create filename 
    dir_name = "plots/"
    base_name = (f.split('/')[-1]).split('.')[0] #removes directory name and extension
    
    if layer!= None:
      description = layer
    else:
      description = "-rec23"
    
    ext_name = "-plot.png"

    # create plot tile
    title_parts = base_name.split("-")
    gen_type = "random stimuli"
    if title_parts[0] == "hmm":
      gen_type = "stimuli containing sequences (HMM)\n"

    plt.title("Recurrent weights in layer 2/3 after showing %s %s to the network.\n Generated on %s." % (title_parts[1], gen_type, title_parts[2]), fontsize=10)


    # save and close figure
    plt.savefig(dir_name + base_name + description + ext_name)
    plt.close()

    f = input("weight matrix filename, or 'done': ")


def main():
  """ creates histogram of weights in given weight matrix file
      default: recurrent weights, use -layer4 or -in23 for other layers
      assumes weight matrix filename generated by ~/bin/autonet
  """
  args = sys.argv[1:]
  if len(args) > 1:
    print("Usage: python3 testplot.py [layer (-layer4 or -in23)]")
    sys.exit(1)
  # flag provided 
  elif len(args) == 1:
    if args[0] == "-layer4" or args[0] == "-in23":
      weights(layer=args[0])
    else:
      print("Error: invalid flag. Options: -layer4, -in23")
      sys.exit(1)
  # no flag (use default)
  else:
    weights()

if __name__ == "__main__":
  main()