import matplotlib as mpl  # https://matplotlib.org/3.3.3/tutorials/introductory/customizing.html


from math import sqrt
default_width = 4.0  # in inches
# default_ratio = (sqrt(5.0) - 1.0) / 2.0  # golden mean
default_ratio = 1/1.6 # golden mean approximation, easy to divie up, 1.6 = 8/5

color_main_text = 'black'
grid_color = 'gray'
grid_color = '#BFBFBF'  # 191/255

ultra_thick_line = 1.6
very_thick_line = 1.2
thick_line = 0.8
semi_thick_line = 0.6
thin_line = 0.4
document_font = 11
base_font_pt = document_font - 1

tick_length = 4

rc = mpl.rcParams

# It is more reliable to set as pt rather than 'small', 'medium' etc.
rc['font.size'] = base_font_pt

# rcParams['axes.titlepad'] = 20
rc['figure.titlesize'] = document_font  # same as document font
rc['figure.facecolor'] = '1.0'

rc['figure.frameon'] = False
rc['figure.figsize'] = [default_width, default_width * default_ratio]  # todo make axis a set size

rc['figure.subplot.left'] =   0.125  # the left side of the subplots of the figure
rc['figure.subplot.right'] =  0.9    # the right side of the subplots of the figure
rc['figure.subplot.bottom'] = 0.11   # the bottom of the subplots of the figure
rc['figure.subplot.top'] =    0.78   # the top of the subplots of the figure
rc['figure.subplot.wspace'] = 0.2    # the amount of width reserved for space between subplots,
rc['figure.subplot.hspace'] = 0.2    # expressed as a fraction of the average axi width

rc['lines.linewidth'] = thick_line  # in my document, 1.6, 0.8, 0.4 base_font_pt are common thickness,

# might want to brighten some of the auxiliary colors
# b r g o y p
#["1400f0", "8b0000", "00820a", "824b00", "788200", "820078"]  ?

col_cyc_rainbow = [0, 5, 1, 3, 4, 2]
col_cyc = ["#1000F0", "#B30000", "#00820A", "#F05F00", "#FFC30B", "#820078"]
cols =         ['b',      'r',      'g',        'o',        'y',    'p']
col_dict = {}
for m, col in enumerate(cols):
    col_dict[col] = col_cyc[m]

rc['axes.prop_cycle'] = mpl.cycler(color=col_cyc)
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
    # rc[xy+'tick.labelcolor'] = color_main_text  # changes text color only # todo not working, until MPL ver 3.4, using 3.1
    # rc[xy+'tick.color'] = grid_color  # changes text AND tick color
    rc[xy+'tick.color'] = color_main_text  # changes text AND tick color
    for mm, fact in zip(('major', 'minor'), (1, 0.75)):  # minor ticks for log plots, make a bit shorter
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

rc['image.cmap'] = 'plasma'

