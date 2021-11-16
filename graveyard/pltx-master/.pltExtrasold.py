import matplotlib as mpl

from math import sqrt
default_width = 4.0  # in inches
# default_ratio = (sqrt(5.0) - 1.0) / 2.0  # golden mean
default_ratio = 1/1.6 # golden mean approximation, easy to divie up, 1.6 = 8/5



# plot font settings
def use_pgf(preamble_f='preamble.tex'):
    with open(preamble_f) as file:
        preamble = file.read()
    mpl.use('pgf')
    mpl.rcParams.update({
        "text.usetex"        : True,
        "text.latex.preamble": preamble,
        "pgf.texsystem": "pdflatex",
        "pgf.rcfonts"  : False,
        "pgf.preamble" : preamble
    })





def dark_scheme():
    bg_color = '#222222'
    fg_color = 'white'
    mpl.rcParams['axes.facecolor'] = bg_color
    mpl.rcParams['figure.facecolor'] = bg_color
    mpl.rcParams['text.color'] = fg_color  # default text color
    mpl.rcParams['ytick.color'] = fg_color   # changes text AND tick color
    mpl.rcParams['xtick.color'] = fg_color  # changes text AND tick color
    mpl.rcParams['axes.labelcolor'] = fg_color # axes label color
    # mpl.rcParams['grid.linestyle'] = ''
    mpl.rcParams['axes.grid'] = True  # dark scheme implies analysis, grid on
    mpl.rcParams['lines.linewidth'] = very_thick_line  # in my document, 1.6, 0.8, 0.4 base_font_pt are common thickness,
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=  # set color cycle to be brighter than normal
                                                 [adjust_lum(col,1.25) for col in col_cyc])


t

color_main_text = 'black'
grid_color = 'gray'
grid_color = '#969696'  # 150/255

ultra_thick_line = 1.6
thick_line = 0.8
thin_line = 0.4
base_font_pt = 10


# It is more reliable to set as pt rather than 'small', 'medium' etc.
mpl.rcParams['font.size'] = base_font_pt

# rcParams['axes.titlepad'] = 20
mpl.rcParams['figure.titlesize'] = base_font_pt + 1 ## 1 size up
mpl.rcParams['figure.facecolor'] = '1.0'
mpl.rcParams['figure.figsize'] = [default_width, default_width * default_ratio]

mpl.rcParams['lines.linewidth'] = thick_line  # in my document, 1.6, 0.8, 0.4 base_font_pt are common thickness,

# might want to brighten some of the auxiliary colors
# b r g o y p
#["1400f0", "8b0000", "00820a", "824b00", "788200", "820078"]  ?

col_cyc_rainbow = [0, 5, 1, 3, 4, 2]
col_cyc = ["#1000F0", "#B30000", "#00820A", "#F05F00", "#FFC30B", "#820078"]
cols =         ['b',      'r',      'g',        'o',        'y',    'p']
col_dict = {}
for m, col in enumerate(cols):
    col_dict[col] = col_cyc[m]

mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=col_cyc)
mpl.rcParams['axes.linewidth'] = thin_line
mpl.rcParams['axes.titlesize'] = base_font_pt
mpl.rcParams['axes.labelsize'] = base_font_pt
mpl.rcParams['axes.edgecolor'] = grid_color
mpl.rcParams['axes.linewidth'] = thin_line

mpl.rcParams['axes.labelcolor'] = color_main_text

mpl.rcParams['axes.xmargin'] = 0  # flushes x axis limits to end of graph
mpl.rcParams['axes.ymargin'] = 0  # comment out so y axis limits are auto adjusts

mpl.rcParams['ytick.labelsize'] = base_font_pt
mpl.rcParams['xtick.labelsize'] = base_font_pt
mpl.rcParams['ytick.color'] = color_main_text  # changes text AND tick color
mpl.rcParams['xtick.color'] = color_main_text  # changes text AND tick color

mpl.rcParams['legend.fancybox'] = False
mpl.rcParams['legend.fontsize'] = base_font_pt
mpl.rcParams['legend.loc'] = 'best'
mpl.rcParams['legend.handlelength'] = 1.0
mpl.rcParams['legend.framealpha'] = 1.0
mpl.rcParams['legend.edgecolor'] = grid_color
mpl.rcParams['legend.frameon'] = True
mpl.rcParams['legend.handletextpad'] = 0.2
# mpl.rcParams['legend.title_fontsize'] = base_font_pt
# mpl.rcParams['legend.alpha'] = 1.0
# mpl.rcParams['legend.borderpad'] = 1

mpl.rcParams['xtick.major.width'] = thin_line
mpl.rcParams['xtick.minor.width'] = thin_line
mpl.rcParams['ytick.major.width'] = thin_line
mpl.rcParams['ytick.minor.width'] = thin_line

mpl.rcParams['xtick.direction'] = 'in'  # more consistent with padding
mpl.rcParams['ytick.direction'] = 'in'
# mpl.rcParams['xtick.length'] = ?


# mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.color'] = grid_color
mpl.rcParams['grid.linewidth'] = thin_line


def set_tick_line_color(ax=None):
    """
    Changes the tick color to that of the grid color
    :param ax: axes to operate note, gca() if None
    :return: None
    """
    if ax is None: ax = mpl.pyplot.gca()
    [tick.tick1line.set_color(grid_color) for tick in ax.yaxis.get_major_ticks()]
    [tick.tick1line.set_color(grid_color) for tick in ax.yaxis.get_minor_ticks()]
    [tick.tick1line.set_color(grid_color) for tick in ax.xaxis.get_major_ticks()]
    [tick.tick1line.set_color(grid_color) for tick in ax.xaxis.get_minor_ticks()]
    [tick.tick2line.set_color(grid_color) for tick in ax.yaxis.get_major_ticks()]  # for right side
    [tick.tick2line.set_color(grid_color) for tick in ax.yaxis.get_minor_ticks()]  # for right side


def set_topright_title(ax=None):
    if ax is None: ax = mpl.pyplot.gca()
    ax.title.set_label_coords(1, 1)  # might wanna use a different metric..?


def rotated_ylabel(label, x=1/2.54, y=0.5/2.54, ax=None, right=False):
    """
    Rotate the y-axis label of a plot and positions it in inches wrt to the top of the frame,
    to the left with x, and above with y
    :param label: Test label. If a multi-line is used, it is recommended that the title height match
    :param x: left offset in inches (measured from top left axis)
    :param y: up offset in inches (measured from top left axis)
    :param ax: axes to modify, if None, current axes
    :return: None
    """
    if ax is None: ax = mpl.pyplot.gca()
    ha='left'
    if right:
        ha='right'

    ax.set_ylabel(label, alpha=1.0, rotation='horizontal', ha=ha, va='bottom')

    bbox = ax.get_position()
    xywh = bbox.bounds
    figwh = mpl.pyplot.gcf().get_size_inches()
    x_off = x/(xywh[2]*figwh[0])
    y_off = y*default_ratio/(xywh[3]*figwh[1])

    if right:
        ax.yaxis.set_label_coords(1-x_off, 1+y_off)  # might wanna use a different metric..
    else:
        ax.yaxis.set_label_coords(-x_off, 1+y_off)  # might wanna use a different metric..

def get_axes_size(fig=None):
    if fig is None: fig = mpl.pyplot.gcf()
    figw, figh = fig.get_size_inches()
    axw = figw*(fig.subplotpars.right-fig.subplotpars.left)
    axh = figh*(fig.subplotpars.top-fig.subplotpars.bottom)
    return axw, axh

"""
First, define axes size and padding
then determine desired padding
"""
def set_ax_size_and_pad(fig=None, w=4.0, h=None, l=0.5, t=0.5, r=None, b=0.5):
    # creates a fig size and layout format based on desired axes size and padding
    if fig is None: fig = mpl.pyplot.gcf()
    if h is None: h = w/1.6  # ~ golden ratio
    if r is None: r = l  # equal left and right padding

    figw = w + r + l
    figh = h + t + b

    rl_rat = 1-w/figw
    l_rat = rl_rat*l/(r+l)
    r_rat = 1 - (rl_rat - l_rat)

    tb_rat = 1-h/figh
    b_rat = tb_rat * b / (t + b)
    t_rat = 1 - (tb_rat - b_rat)

    fig.set_size_inches(figw, figh)
    fig.subplots_adjust(left=l_rat, right=r_rat, bottom=b_rat, top=t_rat)

    # todo work this out for subplots optionally


def set_subp_pad(fig=None, N=2, M=1, w=0.25, h=0.25):
    if fig is None: fig = mpl.pyplot.gcf()
    # ax_list = fig.axes
    # todo get N and M automatically
    # Wax = N * Wsa + (N-1) * Wwh
    # Wax/Wwh = N * Wsa/Wwh + N-1
    # wspace = (Wsa/Wwh)^-1 = ((Wax/Wwh + 1 - N)/N)**-1
    Wax, Hax = get_axes_size(fig)
    fig.subplots_adjust(hspace=M/(Hax/h + 1 - M),
                        wspace=N/(Wax/w + 1 - N))



def append_unit_last_tick(unit='s', ax=None, new_way=True):
    if ax is None: ax = mpl.pyplot.gca()
    if not new_way:
        labels = [item.get_text() for item in ax.get_xticklabels()]
        labels[-1] = labels[-1] + ' ' + unit
        ax.set_xticklabels(labels)
    else:
        labels = ax.get_xticks().tolist()
        labels[-1] = str(labels[-1]) + ' ' + unit
        ax.set_xticklabels(labels)



def scale_ticks(scale, ax=None, xory='y'):
    if ax is None: ax=mpl.pyplot.gca()
    ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:.1f}'.format(x*scale))
    if xory == 'x':
        ax.xaxis.set_major_formatter(ticks)
    else:
        ax.yaxis.set_major_formatter(ticks)

def scale_ticks_func(scale_func, ax=None, xory='y'):
    if ax is None: ax=mpl.pyplot.gca()
    ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:.1f}'.format(scale_func(x)))
    if xory == 'x':
        ax.xaxis.set_major_formatter(ticks)
    else:
        ax.yaxis.set_major_formatter(ticks)

def scale_ticks_func_(scale_func, ax=None, xory='y', last=''):
    if ax is None: ax=mpl.pyplot.gca()
    ticks = ax.get_xticks()
    ticks_new = scale_func(ticks)
    ticks_label_new = ['{0:.1f}'.format(tick) for tick in ticks_new]
    ticks_label_new[-1] = ticks_label_new[-1] + last
    # ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:.1f}'.format(scale_func(x)))
    if xory == 'x':
        # ax.xaxis.set_major_formatter(ticks)
        ax.set_xticklabels(ticks_label_new)
    else:
        ax.yaxis.set_major_formatter(ticks)


# todo check out below for alignemnt
# https://stackoverflow.com/questions/7936034/text-alignment-in-a-matplotlib-legend

def legend_frame(ax=None, leg=None):
    if ax==None:ax = mpl.pyplot.gca()
    if leg is None:
        legends = [c for c in ax.get_children() if isinstance(c, mpl.legend.Legend)]
        for legend in legends:
            legend.get_frame().set_linewidth(thin_line)
    else:
        leg.get_frame().set_linewidth(thin_line)


def set_legend_text_col(leg=None, type='line'):
    if leg is None: leg = mpl.pyplot.legend()
    for handle, text in zip(leg.legendHandles, leg.get_texts()):
        if type == 'line':
            text.set_color(handle.get_color())
        else:
            text.set_color(handle.get_facecolor()[0])


def set_line_legend(ax=None):
    # used for histogram
    if ax is None: ax = mpl.pyplot.gca()
    handles, labels = ax.get_legend_handles_labels()
    new_handles = [mpl.lines.Line2D([], [], c=h.get_edgecolor()) for h in handles]
    mpl.pyplot.legend(handles=new_handles, labels=labels)



def draw_line(ax=None, x=[0,1], y=[0,0], color=grid_color):
    """
    Note: tight_layout cuts this off !!!
    :param x:
    :param ax:
    :return:
    """
    if ax is None: ax = mpl.pyplot.gca()
    import numpy as np
    x, y = np.array([x, y])
    ax.add_line(mpl.lines.Line2D(x, y, lw=thin_line, color=color, alpha=1.0, clip_on=True,
                                 transform=ax.transAxes))


"""
obsolete, these were from the texfig package, probably not good for reports
Returns a figure with an appropriate size and tight layout.
"""
def figure(width=default_width, ratio=default_ratio, pad=0, *args, **kwargs):
    fig = mpl.pyplot.figure(figsize=(width, width * ratio), *args, **kwargs)
    fig.set_tight_layout({
        'pad': pad
    })
    return fig
# https://stackoverflow.com/questions/51405646/matplotlib-ticks-sans-serif-for-all-plots


"""
Returns subplots with an appropriate figure size and tight layout.
"""
def subplots(width=default_width, ratio=default_ratio, *args, **kwargs):
    fig, axes = mpl.pyplot.subplots(figsize=(width, width * ratio), *args, **kwargs)
    fig.set_tight_layout({
        'pad': 0.1
    })
    return fig, axes


def update_prop(handle, orig):
    """
    not sure what it's used for..
    :param handle:
    :param orig:
    :return:
    """
    # https://stackoverflow.com/questions/48391146/change-marker-in-the-legend-in-matplotlib
    handle.update_from(orig)
    handle.set_marker("")
    handle.set_linestyle("-")


"""
OLD WAYS OF GETTING APPROPRIATE AXES SIZE...
"""

def center_axes(ax=None):
    if ax is None: ax = mpl.pyplot.gca()
    r = ax.figure.subplotpars.right
    l = ax.figure.subplotpars.left
    r_ = 1 - r
    l_new = (l+r_)/2.
    r_new = 1-l_new
    mpl.pyplot.subplots_adjust(left=l_new, right=r_new)

def set_ax_size(w, h=None, ratio=default_ratio, ax=None):
    if ax is None: ax = mpl.pyplot.gca()
    #### mpl.pyplot.tight_layout()
    #    do not adjust layout... may results in too tight
    # YOU MAY WANT TO ADJUST FIGURE SPACING
    """ w, h: width, height in inches
    https://stackoverflow.com/questions/44970010/axes-class-set-explicitly-size-width-height-of-axes-in-given-units
    """
    if h is None: h = w*ratio
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)

def pad_hor(pad=5, char='@', ax=None):
    if ax is None: ax = mpl.pyplot.gca()
    ax.set_title(char*pad, loc='right', horizontalalignment='left')
    ax.set_title(char*pad, loc='left', horizontalalignment='right')

def pad_top(pad=5, char='@\n', ax=None):
    if ax is None: ax = mpl.pyplot.gca()
    ax.set_title(char*pad, loc='center')

def pad_bot(pad=5, char='@\n', ax=None):
    if ax is None: ax = mpl.pyplot.gca()
    ax.set_xlabel(char * pad)

def clear_padding(ax=None):
    if ax is None: ax = mpl.pyplot.gca()
    ax.set_title('', loc='right')
    ax.set_title('', loc='left')
    ax.set_xlabel('')
    ax.set_title('', loc='center')


def adjust_lum(color, amount=0.5):
    # https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])




def make_space_above(axes, topmargin=1):
    """ increase figure size to make topmargin (in inches) space for
        titles, without changing the axes sizes"""
    # https://stackoverflow.com/questions/55767312/how-to-position-suptitle
    fig = axes.flatten()[0].figure
    s = fig.subplotpars
    w, h = fig.get_size_inches()

    figh = h - (1-s.top)*h  + topmargin
    fig.subplots_adjust(bottom=s.bottom*h/figh, top=1-topmargin/figh)
    fig.set_figheight(figh)

def draw_center_line(x=0.5, ax=None):
    """
    Note: tight_layout cuts this off !!!
    :param x:
    :param ax:
    :return:
    """
    if ax is None: ax = mpl.pyplot.gca()
    import numpy as np
    x,y = np.array([[0.0-x, 1.5+x], [0.0, 0.0]])

    #fixme use plt.axhline(YCOORD, 0, 1, linestyle='--', linewidth=1, color='gray')  for example
    ax.add_line(mpl.lines.Line2D(x, y, lw=thin_line, color='black', alpha=1.0, clip_on=False,
                                 transform=ax.transAxes))


from mpl_toolkits.axes_grid1 import Divider, Size
def fix_axes_size_in(w, h=None, ratio=default_ratio):
    # DOES NOT WORK WITH PGF??? ONLY WITH PDF
    """
    https://stackoverflow.com/questions/44970010/axes-class-set-explicitly-size-width-height-of-axes-in-given-units
    :param w:
    :param h:
    :param ratio:
    :return:
    """
    if h is None: h = w*ratio
    #lets use the tight layout function to get a good padding size for our axes labels.
    fig = mpl.pyplot.gcf()
    ax = mpl.pyplot.gca()
    fig.tight_layout()
    #obtain the current ratio values for padding and fix size
    oldw, oldh = fig.get_size_inches()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    #work out what the new  ratio values for padding are, and the new fig size.
    neww = w+oldw*(1-r+l)
    newh = h+oldh*(1-t+b)
    newr = r*oldw/neww
    newl = l*oldw/neww
    newt = t*oldh/newh
    newb = b*oldh/newh
    #right(top) padding, fixed axes size, left(bottom) pading
    hori = [Size.Scaled(newr), Size.Fixed(w), Size.Scaled(newl)]
    vert = [Size.Scaled(newt), Size.Fixed(h), Size.Scaled(newb)]
    divider = Divider(fig, (0.0, 0.0, 1., 1.), hori, vert, aspect=False)
    # the width and height of the rectangle is ignored.
    ax.set_axes_locator(divider.new_locator(nx=1, ny=1))
    #we need to resize the figure now, as we have may have made our axes bigger than in.
    fig.set_size_inches(neww,newh)



def dblhist(arr, bins=None, binsC=None, color=None):
    # todo find a way to pass kwargs dict for histogram
    # histargs
    # histCargs

    # bins = np.arange(np.floor(np.min(volts[volts>100])), np.ceil(np.max(volts)), 0.2)
    # binsD = np.arange(np.floor(np.min(volts[volts>100])), np.ceil(np.max(volts)), 0.1)

    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(4, 1)
    ax1 = fig.add_subplot(gs[0:-1, 0])
    ax2 = fig.add_subplot(gs[-1, 0])

    ax1.hist(arr, bins=bins, color=color)  #
    ax2.hist(arr, bins=binsC, histtype='step', cumulative=-1, color=color)  #

    ax2.set_yticks(np.array([0,25,50,75,100])/100*np.size(arr))
    ax2.grid(True)
    # ax1.set_yticks(np.array([0,2.5,5.,7.5,10])/100*np.size(arr))
    ax1.grid(True)

    scale_ticks(100.0 / np.size(arr), ax=ax1)
    scale_ticks(100.0 / np.size(arr), ax=ax2)

    ax2.set_xlim(ax1.get_xlim())

    return fig, ax1, ax2



""" Examples """

# Set an indidual tick number padding (space) and length
# ax.xaxis.get_major_ticks()[1].set_pad(15)
# ax.xaxis.get_major_ticks()[1].tick1line.set_markersize(15)

# draw a 2d line (horizontal, from  [x1,y1] to [x2,y2], in axes data coordinates
# x,y = np.array([[0.0, 0.5117], [0.5117, 0.5117]])
# ax.add_line(mpl.lines.Line2D(x, y, lw=thin_line, color='gray', alpha=1.0, clip_on=True))

# https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/text_alignment.html


# labels = [item.get_text() for item in ax.get_xticklabels()]
# labels[1] = 'Testing'

# def gradient_cycle(num_plots, colormap=plt.cm.viridis, st=0.0, en=1.0):
    # https://matplotlib.org/tutorials/colors/colormaps.html
    # https://jakevdp.github.io/PythonDataScienceHandbook/04.07-customizing-colorbars.html
    # colormap = plt.cm.hot # works well with 0.6  # plt.cm.gist_ncar,

    # for ax in plt.gcf().get_axes():
    #     ax.set_prop_cycle(plt.cycler('color',
    #         [colormap(i) for i in np.linspace(st, en, num_plots)]))  # play around with the values



# set spine bounds extents line length axes
# ax2.spines['left'].set_bounds(-1.1, 1.1)
# shift translate move spines in terms of data coords axes
#  ax.spines['right'].set_position(('data', 10.2))