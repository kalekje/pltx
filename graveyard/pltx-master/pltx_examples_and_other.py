
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


def scale_ticks(scale, ax=None, xory='y'):
    if ax is None: ax=mpl.pyplot.gca()
    ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:.1f}'.format(x*scale))
    if xory == 'x':
        ax.xaxis.set_major_formatter(ticks)
    else:
        ax.yaxis.set_major_formatter(ticks)
