import matplotlib as mpl
mpl.use('agg')
from matplotlib.testing.compare import compare_images
from tempfile import NamedTemporaryFile
import os.path
import pygenometracks.plotTracks

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/test_data/"

browser_tracks = """
[x-axis]

[x-axis]
fontsize=30

[spacer]
height = 0.05

[tads]
file = tad_classification.bed
title = TADs color=bed_rgb; border color = black
display = triangles
border color = black
color = bed_rgb
height = 5

[tads 2]
file = tad_classification.bed
title = TADs orientation=inverted; color=#cccccc; border color=red
display = triangles
border color = red
color = #cccccc
orientation = inverted
height = 3

[spacer]
height = 0.5

[tad state]
file = chromatinStates_kc.bed.gz
height = 1.2
title = bed display=interleaved; labels=off
display = interleaved
labels = off

[spacer]
height = 0.5

[tad state]
file = chromatinStates_kc.bed.gz
height = 0.5
title = bed display=collapsed; color=bed_rgb
display = color from bed rgb
labels = off
color = bed_rgb
display = collapsed

[spacer]
height = 0.5

[test bedgraph]
file = bedgraph_chrx_2e6_5e6.bg
color = blue
height = 4
title = bedgraph color=blue

[test arcs]
file = test.arcs
title = links orientation=inverted
orientation = inverted

[test bigwig]
file = bigwig_chrx_2e6_5e6.bw
color = blue
height = 4
title = bigwig number of bins=2000
number of bins = 2000

[test arcs]
file = test.arcs
color = red
line width = 3
title = links line width=3
height = 4

[test bigwig lines]
file = bigwig_chrx_2e6_5e6.bw
color = red
height = 4
type = line
title = bigwig orientation=inverted; show data range=no
orientation = inverted
show data range = no

[test bigwig lines]
file = bigwig_chrx_2e6_5e6.bw
color = red
height = 4
type = line:0.2
title = bigwig type=line:0.2

[test bigwig points]
file = bigwig_chrx_2e6_5e6.bw
color = black
height = 4
min_value = 0
max_value = 100
type = points:0.5
title = bigwig type=point:0.5; min_value=0;max_value=100

[spacer]
height = 0.5

[genes 2]
file = dm3_genes.bed.gz
height = 10
title = genes (bed12) style=flybase;fontsize=10
style=flybase
fontsize = 10

[spacer]
height = 1

[test gene rows]
file = dm3_genes.bed.gz
height = 3
title = max num rows=3; style=UCSC
fontsize = 8
style = UCSC
gene rows = 3

[spacer]
height = 1

[test bed6]
file = dm3_genes.bed6.gz
height = 7
title = bed6 color=Reds;border color=black; gene rows=10; fontsize=8
fontsize = 8
file_type = bed
color = Reds
border color = black
gene rows = 10

[test bed6]
file = dm3_genes.bed6.gz
height = 15
title = bed6 global max row=yes; fontsize=10
fontsize = 10
file_type = bed
global max row = yes
interval_height = 200

[vlines]
file = tad_classification.bed
type = vlines

"""
with open(ROOT + "browser_tracks.ini", 'w') as fh:
    fh.write(browser_tracks)

tolerance = 13  # default matplotlib pixed difference tolerance


def test_plot_tracks():

    outfile = NamedTemporaryFile(suffix='.png', prefix='pyGenomeTracks_test_', delete=False)
    args = "--tracks {0}/browser_tracks.ini --region chrX:3000000-3500000 --trackLabelFraction 0.2 --width 38 " \
           "--dpi 130 --outFileName  {1}".format(ROOT, outfile.name).split()
    pygenometracks.plotTracks.main(args)
    print("saving test to {}".format(outfile.name))
    res = compare_images(ROOT + '/master_plot.png', outfile.name, tolerance)
    assert res is None, res

    os.remove(outfile.name)
