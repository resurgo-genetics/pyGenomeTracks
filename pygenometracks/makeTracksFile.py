import argparse
import os
import sys

from pygenometracks._version import __version__


def parse_arguments(args=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=('Facilitates the creation of a configuration file for hicPlotTADs. This program takes a list '
                     'of files and does the boilerplate for the configuration file.'))

    # define the arguments
    parser.add_argument('--trackFiles', '-f',
                        help='Files to use in for the tracks. The ending of the file is used to define the type of'
                             'track.',
                        nargs='+',
                        type=argparse.FileType('r'),
                        required=True)

    parser.add_argument('--out', '-o',
                        help='File to save the tracks',
                        metavar='output file',
                        type=argparse.FileType('w'),
                        required=False)

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    return parser


def main(args=None):
    args = parse_arguments().parse_args(args)
    args.out.write("""
[x-axis]
#optional
#fontsize=20
# default is bottom meaning below the axis line
# where=top

[spacer]

""")

    for file_h in args.trackFiles:
        label = ".".join(os.path.basename(file_h.name).split(".")[0:-1])
        if file_h.name.endswith('.bw') or file_h.name.endswith('.bigwig') or file_h.name.endswith('.bigWig'):
            default_values = """
color = #666666
min_value = 0
#max_value = auto
height = 1.5
number of bins = 500
nans to zeros = True
# options are: line, points, fill. Default is fill
# to add the preferred line width or point size use:
# type = line:lw where lw (linewidth) is float
# similary points:ms sets the point size (markersize (ms) to the given float
type = line
# type = line:0.5
# type = points:0.5
#optional in case it can not be guessed by the file ending
file_type = bigwig
"""
            args.out.write("\n[{label}]\nfile={file}\ntitle={label}{default_values}".
                           format(label=label, file=file_h.name, default_values=default_values))

            sys.stdout.write("Adding bigwig file: {}\n".format(file_h.name))

        elif file_h.name.endswith('.bg') or file_h.name.endswith('.bedgraph') or file_h.name.endswith('.bedGraph'):
            default_values = """
color = green
height = 0.2
file_type = bedgraph
"""
            args.out.write("\n[{label}]\nfile={file}\ntitle={label}{default_values}".
                           format(label=label, file=file_h.name, default_values=default_values))

            sys.stdout.write("Adding bedgraph file: {}\n".format(file_h.name))

        elif file_h.name.endswith('.bed'):
            default_values = """

# if the type=genes is given
# the the file is interpreted as gene
# file. If the bed file contains the exon
# structure (bed 12) then this is plotted. Otherwise
# a region **with direction** is plotted.
color = darkblue
#if color is a valid colormap name (like RbBlGn), then the score is mapped
# to the colormap. If the color is simply a color name, then this color is used and the score is not considered.
# For this option to work, the min_value and max_value for the score need to be set
#color = RdYlBu
#min_value=0
#max_value=100
height = 5
# to turn off/on printing of labels
labels = off
# optional. If not given is guessed from the file ending
file_type = bed
# optional: font size can be given to override the default size
fontsize = 10
# display collapsed is useful to plot chromatin states one after the other. It is expected that the bed regions do
# not overlap
# display = collapsed
# display interleaved is useful to plot TADs. Also, it is expected that the bed regions do not overlap
# display = interleaved
#optional, default is black
#border_color = black
# style to plot the genes when they have exon information
#style = UCSC
#style = flybase
# maximum number of gene rows to be plotted. This
# field is useful to limit large number of close genes
# to be printed over many rows. When several images want
# to be combined this must be set to get equal size, otherwise, on each image the height of each gene changes
#gene rows = 10
# by default the ymax is the number of
# rows occupied by the genes in the region plotted. However,
# by setting this option, the global maximum is used instead.
# This is useful to combine images that are all consistent and
# have the same number of rows.
#global max row = yes"""
            args.out.write("\n[{label}]\nfile={file}\ntitle={label}{default_values}".
                           format(label=label, file=file_h.name, default_values=default_values))

            sys.stdout.write("Adding bed file: {}\n".format(file_h.name))

        elif file_h.name.endswith('.h5') or file_h.name.endswith('.npz'):
            default_values = """
colormap = RdYlBu_r
depth = 100000
#min_value =2.8
#max_value = 3.0
transform = log1p
#boundaries_file = boundaries_example
#type = arcplot
#type = interaction
#optional in case it can not be guessed by the file ending
file_type = hic_matrix
# show masked bins plots as white lines
# those bins that were not used during the correction
# the default is to extend neighboring bins to
# obtain an aesthetically pleasant output
show_masked_bins = yes
# optional if the values in the matrix need to be scaled the
# following parameter can be used. This is useful to plot multiple hic-matrices on the same scale
# scale factor = 1
"""
            args.out.write("\n[{label}]\nfile={file}\ntitle={label}{default_values}".
                           format(label=label, file=file_h.name, default_values=default_values))

            sys.stdout.write("Adding HiCExplorer matrix file: {}\n".format(file_h.name))

        elif file_h.name.endswith('.bm') or file_h.name.endswith('.bedgraphmatrix'):
            default_values = """
# a bedgraph matrix file is like a bedgraph, except that per bin there
# are more than one value separated by tab: E.g.
# chrX	18279	40131	0.399113	0.364118	0.320857	0.274307
# chrX	40132	54262	0.479340	0.425471	0.366541	0.324736
#orientation = inverted
#min_value = 0.10
#max_value = 0.70
# if type is set as lines, then the TAD score lines are drawn instead
# of the matrix
# set to lines if a heatmap representing the matrix
# is not wanted
type = lines
file_type = bedgraph_matrix
plot horizontal lines=False
height=8
"""
            args.out.write("\n[{label}]\nfile={file}\ntitle={label}{default_values}".
                           format(label=label, file=file_h.name, default_values=default_values))

            sys.stdout.write("Adding bedgraph matrix matrix file: {}\n".format(file_h.name))

        else:
            sys.stdout.write("WARNING: file format not recognized for: {}\n".format(file_h.name))