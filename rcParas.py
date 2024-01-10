# https://matplotlib.org/stable/tutorials/introductory/customizing.html
import matplotlib as mpl
from . import colors
from .defaults import *
rc = mpl.rcParams

# It is more reliable to set as pt rather than 'small', 'medium' etc.
rc['font.size'] = base_font_pt

# rcParams['axes.titlepad'] = 20
rc['figure.titlesize'] = document_font  # same as document font
rc['figure.facecolor'] = '1.0'

try:
    rc['axes.titlelocation'] = 'left'  # title location
except:
    pass  # not valid for some reason

rc['figure.max_open_warning'] = 128
rc['figure.frameon'] = False
rc['figure.figsize'] = [width_default, width_default * ratio_default]  # todo make axis a set size
# todo should set these based on calculations
rc['figure.subplot.left'] =   0.125  # the left side of the subplots of the figure
rc['figure.subplot.right'] =  0.9    # the right side of the subplots of the figure
rc['figure.subplot.bottom'] = 0.11   # the bottom of the subplots of the figure
rc['figure.subplot.top'] =    0.78   # the top of the subplots of the figure
rc['figure.subplot.wspace'] = 0.2    # the amount of width reserved for space between subplots,
rc['figure.subplot.hspace'] = 0.2    # expressed as a fraction of the average axi width

rc['savefig.transparent'] = True

rc['lines.linewidth'] = thick_line  # in my document, 1.6, 0.8, 0.4 base_font_pt are common thickness,


rc['axes.prop_cycle'] = mpl.cycler(color=colors.col_cyc)
rc['axes.linewidth'] = thin_line
rc['axes.titlesize'] = base_font_pt
rc['axes.labelsize'] = base_font_pt
rc['axes.edgecolor'] = grid_color
rc['axes.linewidth'] = thin_line

rc['axes.labelcolor'] = color_main_text

# prefer very small margins, but adjust the spines to create room
rc['axes.xmargin'] = 0.005/1.6
rc['axes.ymargin'] = 0.005

rc['axes.spines.top'] = False
rc['axes.spines.right'] = False

rc['grid.color'] = grid_color
rc['grid.linewidth'] = thin_line

for xy in 'xy':
    rc[xy+'tick.direction'] = 'in'  # more consistent with padding
    rc[xy+'tick.labelsize'] = base_font_pt
    try:
        rc[xy+'tick.color'] = grid_color  # changes text AND tick color
        rc[xy+'tick.labelcolor'] = color_main_text  # works for MPL ver 3.4, using 3.1
    except:
        rc[xy + 'tick.color'] = color_main_text  # changes text AND tick color
    for mm, fact in zip(('major', 'minor'), (1, 0.5)):  # minor ticks for log plots, make a bit shorter
        rc[xy+'tick.'+mm+'.width'] = thin_line  # in pts
        rc[xy+'tick.'+mm+'.size'] = tick_length*fact  # in pts



# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
rc['legend.fontsize'] = base_font_pt
rc['legend.loc'] = 'upper right'
rc['legend.fancybox'] = False
rc['legend.framealpha'] = 1.0
rc['legend.facecolor'] = 'white'
rc['legend.edgecolor'] = 'white'
rc['legend.frameon'] = False

rc['legend.handlelength'] = 1.0
rc['legend.handletextpad'] = 0.2
rc['legend.borderpad'] = 0.2

# todo adjust padding and stuff
# rc['legend.title_fontsize'] = base_font_pt

rc['image.cmap'] = colors.cmap_heat

