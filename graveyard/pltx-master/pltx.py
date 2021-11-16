import matplotlib as mpl
import numpy as np

# todo add decorator to check for ax and fig in kwargs and use gcf() and gca() if none fixme hellow

from .pltx_fmt import *

import functools as ft
import operator as op

# https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
def rgetattr(obj, attr, *args):  # recursive getattr, works for nested attr
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return ft.reduce(_getattr, [obj] + attr.split('.'))

import os
__this_file_dir__ = os.path.dirname(os.path.realpath(__file__))

def use_pgf(pre='preamble',font='sans', eng='pdf'):  # to enable latex text formatting
    preamble_file = '-'.join([pre, eng, font])+'.tex'
    with open(os.path.join(__this_file_dir__ , preamble_file)) as file:
        preamble = file.read().replace('\n', '')  # ensure comments are removed # todo do a regex replace to remove all comments from latex file???
    mpl.rc('font', family=(font=='sans')*'sans-' + 'serif')  # set non-math font correctly
    mpl.use('pgf')
    mpl.rcParams.update({
        "pgf.rcfonts": False,
        "pgf.texsystem": eng+"latex",
        "pgf.preamble" : preamble,
    })
    # lua serif and sans: math content works, body test does not
    # longer compile but improved memory, pdflatex can't make hexbin plots
    # todo must get cmbright to work, it is not working with lua,



def dark_scheme(grid=False):
    bg_color = '#222222'
    fg_color = 'white'
    mpl.rcParams['axes.facecolor'] = bg_color
    mpl.rcParams['figure.facecolor'] = bg_color
    mpl.rcParams['savefig.facecolor'] = bg_color
    mpl.rcParams['text.color'] = fg_color  # default text color
    mpl.rcParams['ytick.color'] = fg_color   # changes text AND tick color
    mpl.rcParams['xtick.color'] = fg_color  # changes text AND tick color
    mpl.rcParams['axes.labelcolor'] = fg_color # axes label color
    # mpl.rcParams['grid.linestyle'] = ''
    mpl.rcParams['axes.grid'] = grid  # dark scheme implies analysis, grid on
    mpl.rcParams['lines.linewidth'] = thick_line  # in my document, 1.6, 0.8, 0.4 base_font_pt are common thickness,
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=  # set color cycle to be brighter than normal
                                                 [adjust_lum(col,1.25) for col in col_cyc])


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


def use_rainbow():
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=col_cyc[col_cyc_rainbow])






# Figures and Axes sizing


def get_axes_size(fig=None):
    if fig is None: fig = mpl.pyplot.gcf()
    figw, figh = fig.get_size_inches()
    axw = figw*(fig.subplotpars.right-fig.subplotpars.left)
    axh = figh*(fig.subplotpars.top-fig.subplotpars.bottom)
    return axw, axh



def set_ax_size_and_pad(fig=None, w=4.0, h=None, l=0.75, t=0.5, r=None, b=0.5):
    # creates a fig size and layout format based on desired axes size and padding, better for consistent ax size
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
    # todo work this out for subplots optionally? -- eg choose ax size for each subplot and spec padding, create fig size


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





# Titles and labels

def set_topright_title(ax=None):
    ax = ax or mpl.pyplot.gca()
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
    ax = ax or mpl.pyplot.gca()
    ha='left'
    if right:
        ha='right'
        x = -x
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
        # todo ensure this is place on top of the axis line





# Legends

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


def set_hist_legend(ax=None):
    # used for histogram
    ax = ax or mpl.pyplot.gca()
    handles, labels = ax.get_legend_handles_labels()
    new_handles = [mpl.lines.Line2D([], [], c=h.get_edgecolor()) for h in handles]
    mpl.pyplot.legend(handles=new_handles, labels=labels)





# Lines and Ticks

def try_float(x):
    try:
        return float(x)
    except:
        return x


def make_ticks(ext, step):
    # makes a np range between two nubers with appropriate step
    return np.arange(ext[0], ext[1]*(1+0.0001), step)


def draw_line(ax=None, x=[0,1], y=[0,0], color=grid_color):
    """
    Note: tight_layout cuts this off !!!
    :param x:
    :param ax:
    :return:
    """
    ax = ax or mpl.pyplot.gca()
    import numpy as np
    x, y = np.array([x, y])
    ax.add_line(mpl.lines.Line2D(x, y, lw=thin_line, color=color, alpha=1.0, clip_on=True,
                                 transform=ax.transAxes, zorder=1))


def add_gridline(val, ax=None, d='v'):
    ax = ax or mpl.pyplot.gca()
    if not isinstance(val, list): val = [val]
    for v in val:
        getattr(ax, 'ax'+d+'line')(v, lw=0.4, color=grid_color, zorder=1)
    ax.set_axisbelow(True)

    # ax.draw() # maybe this invokes z order # todo investigate


def add_callout(ax=None, loc=[], where='lb', tick=False, log=''):
    # todo investigate label setting, for now, rely on settign ticks manyaly
    ax = ax or mpl.pyplot.gca()
    if 'x' in log:
        x_a = np.log(loc[0]/ax.get_xlim()[0])/np.log(1/ft.reduce(op.sub, ax.get_xlim()))
    else:
        x_a = (loc[0]-ax.get_xlim()[0])/-(ft.reduce(op.sub, ax.get_xlim()))
    if 'y' in log:
        y_a = np.log(loc[1]/ax.get_ylim()[0])/np.log(1/(ft.reduce(op.truediv, ax.get_ylim())))
    else:
        y_a = (loc[1]-ax.get_ylim()[0])/-(ft.reduce(op.sub, ax.get_ylim()))
    for a in where:
        if a == 'l':
            draw_line(ax=ax, x=[0, x_a], y=[y_a, y_a])
            if tick:
                ax.set_yticks(list(ax.get_yticks()) +[loc[1]])
                if isinstance(tick, str):
                    ax.set_yticklabels(list(map(op.methodcaller('get_text'), ax.get_yticklabels())) + [str(loc[1])])
        if a == 'b':
            draw_line(ax=ax, x=[x_a, x_a], y=[0, y_a])
            if tick:
                ax.set_xticks(np.concatenate([ax.get_xticks(), [loc[0]]]))
                if isinstance(tick, str):
                # ax.set_xticklabels(np.concatenate([ax.get_xticklabels(), [str(loc[0])]]))
                    ax.set_yticklabels([list(map(op.methodcaller('get_text'),ax.get_yticklabels())), [str(loc[1])]])



# ax.draw() # maybe this invokes z order # todo investigate




def shorten_spines(ax=None, which='l', opt=1):
    ax = ax or mpl.pyplot.gca()
    for loc, a in zip(['left', 'right', 'top', 'bottom'],'yyxx'):
        ticks = getattr(ax, 'get_'+a+'ticks')()  # Get locations and labels
        if opt == 2:
            ax.spines[loc].set_bounds(ticks[0], ticks[-1])
        elif opt == 3:
            ax.spines[loc].set_bounds(ticks[1], ticks[-2])
        elif opt:
            ax.spines[loc].set_bounds(np.min(ticks), np.max(ticks))


def fmt_ticks(func=lambda x: x, ax=None, xy='y', fmt='.1f', applast='', app=None):
    # todo allow dynamic fmt spec?
    # todo allow scaling of ticks?
    ax = ax or mpl.pyplot.gca()
    if any([fmt, applast, app]):
        for xory in xy:
            ticks = map(try_float, getattr(ax, 'get_'+xory+'ticks')())
            ticks_new = [('{0:'+fmt+'}').format(func(t)) if isinstance(t, (float, int)) else t for t in ticks]
            if app:
                for k, v in app.items():
                    ticks_new[k] = ticks_new[k] + v
            elif applast:
                ticks_new[-1] = ticks_new[-1] + applast
            getattr(ax, 'set_'+xory+'ticklabels')(ticks_new)


def hide_ticklabel(ax=None, xy='x', vals=None, slice='', inds=None):
    # todo add option to select by value
    ax = ax or mpl.pyplot.gca()
    if 'e' in slice:
        slice = (0, 0, 2)  # even slice, takes 0, 2, 4, etc
    if 'o' in slice:
        slice = (1, 0, 2) # odd slice
    if 'a' in slice:
        slice = (0, 0, 1) # hide all
    labels = getattr(ax, 'get_'+xy+'ticklabels')()
    if slice:
        for i in range(slice[0], len(labels)-slice[1], slice[2]):
            labels[i] = ''
    if inds:
        if not isinstance(inds, list):
            inds = [inds]
        for i in inds:
            labels[i] = ''
    getattr(ax, 'set_'+xy+'ticklabels')(labels)


def set_tick_line_color(ax=None, color=grid_color):
    """
    Changes the tick color to that of the grid color
    :param ax: axes to operate note, gca() if None
    :return: None
    """
    ax = ax or mpl.pyplot.gca()
    for n in '12':
        for xy in 'xy':
            for mm in ('major', 'minor'):
                [rgetattr(tick,'tick'+n+'line.set_color')(color)
                 for tick in rgetattr(ax, xy+'axis.get_'+mm+'_ticks')()]
    # [tick.tick1line.set_color(color) for tick in ax.yaxis.get_major_ticks()]
    # [tick.tick1line.set_color(color) for tick in ax.yaxis.get_minor_ticks()]
    # [tick.tick1line.set_color(color) for tick in ax.xaxis.get_major_ticks()]
    # [tick.tick1line.set_color(color) for tick in ax.xaxis.get_minor_ticks()]
    # [tick.tick2line.set_color(color) for tick in ax.yaxis.get_major_ticks()]  # for right side
    # [tick.tick2line.set_color(color) for tick in ax.yaxis.get_major_ticks()]  # for right side
    # [tick.tick2line.set_color(color) for tick in ax.xaxis.get_minor_ticks()]  # for top side
    # [tick.tick2line.set_color(color) for tick in ax.xaxis.get_major_ticks()]  # for top side
    # todo matplotlib 3.4 > allows rc ticklabel.color for this


def add_right_yaxis(ax, **kwargs):
    ax_new = ax.twinx()
    ax_new.spines['right'].set_position(('outward', tick_length))  # messes up tick color if done later
    kwargs.update(dict(ax=ax_new, xy='y'))
    format_spines_ticks(**kwargs)
    ax_new.set_ylim(ax.get_ylim()) # if plots are going to have different units, should be on a seprate plot
    ax_new.set_xlim(ax.get_xlim())
    ax_new.spines['right'].set_visible(True)
    ax_new.spines['left'].set_visible(False)
    ax_new.spines['top'].set_visible(False)
    ax_new.spines['bottom'].set_visible(False)
    ticks = ax_new.get_yticks()
    ax_new.spines['right'].set_bounds(np.min(ticks), np.max(ticks))
    ax_new.set_axisbelow(True)
    return ax_new



def add_top_xaxis(ax, **kwargs):
    ax_new = ax.twiny()
    ax_new.spines['top'].set_position(('outward', tick_length))  #
    kwargs.update(dict(ax=ax_new, xy='x'))
    format_spines_ticks(**kwargs)
    ax_new.set_ylim(ax.get_ylim()) #
    ax_new.set_xlim(ax.get_xlim())
    ax_new.spines['top'].set_visible(True)
    ax_new.spines['right'].set_visible(False)
    ax_new.spines['left'].set_visible(False)
    ax_new.spines['bottom'].set_visible(False)
    ticks = ax_new.get_xticks()
    ax_new.spines['top'].set_bounds(np.min(ticks), np.max(ticks))
    ax_new.set_axisbelow(True)
    return ax_new


def set_plot_extents(ax=None, xy='x', ext=[], buff=0.005):
    # sets limits, adds a small buffer (default is very small, 1%)
    ax = ax or mpl.pyplot.gca()
    rat = 1.0
    if 'x' in xy:
        w, h = get_axes_size()
        rat = 1.0*h/w
    min, max = ext
    pad = buff*(max - min)*rat
    getattr(ax, 'set_'+xy+'lim')(min-pad, max+pad)  # use small padding to avoid chopping signal


def outward_spines(ax=None, xy='x'):
    for xory in xy:
        if xory == 'x': sides = ('bottom', 'top')
        if xory == 'y': sides = ('left', 'right')
        for side in sides:
            ax.spines[side].set_position(('outward', tick_length))

def zeroed_xspine(ax=None):
    ax.spines['bottom'].set_position(('data', 0.0))
    ax.tick_params(axis='x', direction='inout')

def get_data_extents(x=None, y=None, ax=None):
    # todo consider making this general so it might work with hexbin plot or histogram, for example
    if (not x and not y):
        ax = ax or mpl.pyplot.gca()
    # pass
    # todo: option to return max and min from a series of x's
    x_max, y_max = -1e9, -1e9
    x_min, y_min = 1e9, 1e9
    for l in ax.get_lines():
        x_dat, y_dat = l.get_xdata(), l.get_ydata()
        x_max = np.max([x_max, np.nanmax(x_dat)])
        y_max = np.max([y_max, np.nanmax(y_dat)])
        x_min = np.min([x_min, np.nanmin(x_dat)])
        y_min = np.min([y_min, np.nanmin(y_dat)])
    return x_min, x_max, y_min, y_max




# todo add the functionality of doing this for all figures?

def format_spines_ticks(ax=None, xy='x',
                        ext=None,  # extents of plot area, small buffer added, graph exceeding is clipped off
                        ticks=None, ticklabels=None,  # specify exact ticks and labels
                        fmt='.1f', app=None, hideslice='',  # tick format if exact not specified, hide some of them, append unit dict
                        shorten=1,  # shorten spines to last tick
                        tick_col=grid_color,
                        zerox=False):  # change tick color but not the label
                        # todo add option for top or right line
    ax = ax or mpl.pyplot.gca()
    if ticks is not None:
        getattr(ax, 'set_'+xy+'ticks')(ticks)
    if ticklabels is not None:
        getattr(ax, 'set_'+xy+'ticklabels')(ticklabels)
    else:
        fmt_ticks(ax=ax, xy=xy, fmt=fmt, app=app)
    if hideslice:
        hide_ticklabel(ax=ax, xy=xy, slice=hideslice)
    if ext:
        set_plot_extents(ax=ax, xy=xy, ext=ext)
        # set_plot_extents(ax=ax, xy=xy, ext=ext, buff=0.0) # todo testing for semi log
    if shorten:
        shorten_spines(ax=ax, opt=shorten)
    if zerox and xy == 'x':
        zeroed_xspine(ax)
    else:
        outward_spines(ax=ax, xy=xy)
    set_tick_line_color(ax=ax, color=tick_col)  # must be after spines are adjusted
    ax.set_axisbelow(True)



def set_plot_extents_old(ax=None, x=None, y=None,
             m='auto', buff=0.01):
    ax = ax or mpl.pyplot.gca()

    w, h = get_axes_size()
    rat = 1.0*h/w

    # todo auto calculate extents if not passed, use above function

    if x:
        xmin, xmax = x
        xbuff = buff*(xmax-xmin)*rat
        ax.set_xlim(xmin-xbuff, xmax+xbuff)
    if y:
        ymin, ymax = y
        ybuff = buff*(ymax-ymin)
        ax.set_ylim(ymin-ybuff, ymax+ybuff)
    # small buffer is used to avoid chopping parts of line off

    if m == 'auto':
        ax.spines['bottom'].set_position(('axes', -0.03))
        ax.spines['left'].set_position(('axes', -0.03*rat))  # same distance as bottom
    elif isinstance(m, list):  # todo maybe incorporate other options
        ax.spines['bottom'].set_position(('axes', m[1]))
        ax.spines['left'].set_position(('axes', m[0]))

