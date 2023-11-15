"""

"""

# todo make these functions work for log plots
import itertools

import numpy as np
import matplotlib as mpl

from .defaults import *
from .sizing import get_axes_size

import functools as ft, operator as op
# https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
def rgetattr(obj, attr, *args):  # recursive getattr, works for nested attr
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return ft.reduce(_getattr, [obj] + attr.split('.'))




def applyToAxes(func):
    """
    allow a function with first arg as an "ax" to accept:
     - single ax
     - list or tuple or np.array of axes, apply function to each iteratively
     - figure, apply function to all axes in figure iteratively
    - note: functions likely have ax=None, which will apply function to current axes (gca) if no ax is passed
    """
    def wrapper(*args, **kwargs):
        applyAxes = False

        if kwargs.get('ax') is not None:
            axs = kwargs['ax']
            kwargs.pop('ax')
            argsother = tuple()
            if args:
                raise Exception('pltx.applyToAxes: PASSED ax kw and args, bad')
        elif args:
            if isinstance(args, tuple):
                axs = args[0]
                argsother = tuple(args[1:])
            else:
                axs = args
                argsother = tuple()
        else:
            print('pltx.applyToAxes: argument error')

        if isinstance(axs, mpl.figure.Figure):
            axs = np.array(axs.axes).flatten()
        elif isinstance(axs, (mpl.axes.Axes, list, tuple, np.ndarray)):
            axs = np.array(axs).flatten()
        else:
            raise Exception('pltx.applyToAxes: bad axs type')

        for ax in axs:
            func(ax, *argsother, **kwargs)

    return wrapper


def try_float(x):
    try:
        return float(x)
    except:
        return x

def try_int_none(x):
    try:
        return int(x)
    except:
        return None



"""
Lines, spines, and ticks
"""

def make_ticks(ext=[], step=1, xy='', ax=None):
    ax = ax or mpl.pyplot.gca()
    # makes a np range between two nubers with appropriate step
    # if xy and ax is given, will give ticks set to extents of data
    if xy:
        x_min, x_max, y_min, y_max = get_data_extents(ax=ax)
        return [locals()[xy+'_min'], 0, locals()[xy+'_max']]
    if ax:
        pass # todo call autoticks here with min and max
    return np.arange(ext[0], ext[1]*(1+0.0001), step)

@applyToAxes
def draw_line(ax=None, x=[0,1], y=[0,0], color=grid_color):
    ax = ax or mpl.pyplot.gca()
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

@applyToAxes # todo
def add_gridline(ax=None, val=0, d='h'):
    ax = ax or mpl.pyplot.gca()
    if not isinstance(val, list): val = [val]
    for v in val:
        getattr(ax, 'ax'+d+'line')(v, lw=0.4, color=grid_color, zorder=1)
    ax.set_axisbelow(True)
    return ax
    # ax.draw() # maybe this invokes z order # todo investigate

@applyToAxes
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
        if a == 'r':
            draw_line(ax=ax, x=[x_a, 1.0], y=[y_a, y_a])
            if tick:
                ax.set_yticks(list(ax.get_yticks()) + [loc[1]])
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



@applyToAxes
def shorten_spines(ax=None, which='l', opt=1):
    ax = ax or mpl.pyplot.gca()
    for loc, a in zip(['left', 'right', 'top', 'bottom'],'yyxx'):
        ticks = getattr(ax, 'get_'+a+'ticks')()  # Get locations and labels
        if np.size(ticks) and ax.spines[loc].get_visible():
            if opt == 2:
                ax.spines[loc].set_bounds(ticks[0], ticks[-1])
            elif opt == 3:
                ax.spines[loc].set_bounds(ticks[1], ticks[-2])
            elif opt:
                ax.spines[loc].set_bounds(np.min(ticks)-np.abs(np.min(ticks))/100000.,
                                          np.max(ticks)+np.abs(np.min(ticks))/100000.)

@applyToAxes
def fmt_ticks(ax=None, func=lambda x: x,  xy='y', fmt='.1f', app=None):
    # todo allow dynamic fmt spec?
    # todo allow scaling of ticks?
    ax = ax or mpl.pyplot.gca()
    if any([fmt, app]):
        for xory in xy:
            ticks = map(try_float, getattr(ax, 'get_'+xory+'ticks')())
            ticks_new = [('{0:'+fmt+'}').format(func(t)) if isinstance(t, (float, int)) else t for t in ticks]
            if app:
                if not isinstance(app, dict):
                    app = {-1: app}  # assume appending to last tick
                for k, v in app.items():
                    ticks_new[k] = ticks_new[k] + v
            getattr(ax, 'set_'+xory+'ticklabels')(ticks_new)

@applyToAxes
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

@applyToAxes
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
    return ax



def copy_lines_invs(ax1, ax2):
    for l in ax1.get_lines():
        x_dat, y_dat = l.get_xdata(), l.get_ydata()
        ax2.plot(x_dat, y_dat, alpha=0.0)

@applyToAxes
def move_right_yaxis(ax=None, pad=None):
    ax = ax or mpl.pyplot.gca()
    ax.yaxis.tick_right()
    ax.spines['right'].set_visible(True)
    ax.spines['left'].set_visible(False)
    if pad:
        pad_right_ticks(ax, pad, True)
    return ax

@applyToAxes
def pad_right_ticks(ax=None, pad=2, ppc=5, onlyright=True, ticks=None, fmt=None):
    if not onlyright or ax.spines['right'].get_visible():
        if ticks:
            pad += ppc*max([len(str(try_int_none(x) or '')) for x in ticks])
            pad += int(fmt[1])*ppc + 2 *(int(fmt[1]) > 0)
            # todo extract number
            # todo need format changin her
            # todo need a way to map decimal chars, make smarter, account for formatting
            # print(pad, ticks)
        ax.yaxis.set_tick_params(pad=pad)
        for label in ax.yaxis.get_ticklabels():
            label.set_horizontalalignment('right')


@applyToAxes
def move_top_xaxis(ax=None):
    ax = ax or mpl.pyplot.gca()
    ax.xaxis.tick_top()
    ax.spines['top'].set_visible(True)
    ax.spines['bottom'].set_visible(False)
    return ax

@applyToAxes
def add_right_yaxis(ax=None, plotinv=True, **kwargs):
    ax = ax or mpl.pyplot.gca()
    # this adds a double axis, doesnt move one
    ax_new = ax.twinx()
    if plotinv:
        copy_lines_invs(ax, ax_new)
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


@applyToAxes
def add_top_xaxis(ax=None, plotinv=False, **kwargs):
    ax = ax or mpl.pyplot.gca()
    # this adds a double axis, doesnt move one
    ax_new = ax.twiny()
    if plotinv:
        copy_lines_invs(ax, ax_new)
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


@applyToAxes
def set_plot_extents(ax=None, xy='x', ext=[], buff=0.000001):
    # sets limits, adds a small buffer (default is very small, 1%)
    ax = ax or mpl.pyplot.gca()
    rat = 1.0
    if 'x' in xy:
        w, h = get_axes_size()
        rat = 1.0*h/w
    min, max = ext
    pad = buff*(max - min)*rat
    getattr(ax, 'set_'+xy+'lim')(min-pad, max+pad)  # use small padding to avoid chopping signal
    return ax

# no wrapper here, intended to be applied to multiple!!!
def add_top_right_spines_subp(axs, hideinterior=True, pad=None): # todo auto detect shape etc
    if isinstance(axs, mpl.figure.Figure): axs = axs.axes # todo need to get shape with nrows ncols1!!
    axs_top = [move_top_xaxis(ax) for ax in axs[0, :]]
    axs_right = [move_right_yaxis(ax, pad=pad) for ax in axs[:, -1]]
    if hideinterior:
        hide_interior_spines(axs)
    return axs_top, axs_right

# no wrapper here!!!
def hide_interior_spines(axs):
    if isinstance(axs, mpl.figure.Figure): axs = axs.axes # todo need to get shape with nrows ncols1!!
    # axs is 2d axs
    for ax in axs[:,1:].flatten():
        ax.spines['left'].set_visible(False)
        ax.set_yticks([])
    for ax in axs[:-1,:].flatten():
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])

@applyToAxes
def outward_spines(ax=None, xy='x'):
    ax = ax or mpl.pyplot.gca()
    for xory in xy:
        if xory == 'x': sides = ('bottom', 'top')
        if xory == 'y': sides = ('left', 'right')
        for side in sides:
            ax.spines[side].set_position(('outward', tick_length))
            ax.spines[side].set_zorder(0.5)
    return ax


@applyToAxes
def hug_spines(ax=None, xy='x'):
    ax = ax or mpl.pyplot.gca()
    for xory in xy:
        if xory == 'x': sides = ('bottom', 'top')
        if xory == 'y': sides = ('left', 'right')
        for side in sides:
            ax.spines[side].set_position(('outward', 0))
            ax.spines[side].set_zorder(0.5)
    return ax



@applyToAxes
def zeroed_spine(ax=None, xy='x'):
    ax = ax or mpl.pyplot.gca()
    ax.spines[{'x':'bottom','y':'left'}[xy]].set_position(('data', 0.0))
    ax.spines[{'x': 'bottom', 'y': 'left'}[xy]].set_zorder(0.5)
    ax.tick_params(axis=xy, direction='inout')
    quick_axis_format(ax, outward=False)


def get_data_extents(ax=None):
    # todo consider making this general so it might work with any array or hexbin plot or histogram, for example
    # if (not x and not y):
    # pass
    # todo: option to return max and min from a series of x's
    ax = ax or mpl.pyplot.gca()
    x_max, y_max = -1e9, -1e9
    x_min, y_min = 1e9, 1e9
    for l in ax.get_lines():
        x_dat, y_dat = l.get_xdata(), l.get_ydata()
        x_max = np.max([x_max, np.nanmax(x_dat)])
        y_max = np.max([y_max, np.nanmax(y_dat)])
        x_min = np.min([x_min, np.nanmin(x_dat)])
        y_min = np.min([y_min, np.nanmin(y_dat)])
    return x_min, x_max, y_min, y_max


def subp_same_ext(axs=None, x=None, y=None, autofmt=True, autotick=True):
    """
    set all axes in a fig to the same data extents
    if x or y is True, it will set the extends to the abs max among all lines
    if x or y is a list, it sets respective axis to those extents
    """
    if autotick is True:
        autotick = 'xy'
    elif not autotick:
        autotick = ''
    axs = axs or mpl.pyplot.gcf()
    if isinstance(axs, mpl.figure.Figure):
        axs = axs.axes
    if x is True or y is True:
        minmaxs = np.empty((0, 4), float)
        for ax in axs:
            minmaxs = np.append(minmaxs, [list(get_data_extents(ax))], axis=0)
        mm = {}
        for n, (xy, m) in enumerate(itertools.product('xy',['min','max'])):
            mm[xy+m] = getattr(np, m)(minmaxs[:,n])  # np.min(..
    for n, ax in enumerate(axs):
        d = dict(x=x,y=y)
        for xy in 'xy':
            if locals()[xy]:
                if locals()[xy] is True:
                    d[xy] = [mm[xy+'min'], mm[xy+'max']]
            if xy in autotick:
                set_auto_tick(ax, xy=xy, ticks=minmaxs[n][0+2*(xy=='y'):2+2*(xy=='y')].tolist(),
                              ext=d[xy])
            set_plot_extents(ax, xy=xy, ext=d[xy])
        if autofmt:
            quick_axis_format(ax)

@applyToAxes
def set_auto_tick(ax, xy='x', ticks=None, ext=None):
    if ticks is None:
        mm = get_data_extents(ax) # x_min, x_max, y_min, y_max
        ticks = list(mm)[0+2*(xy=='y'):2+2*(xy=='y')] # todo test this
    if np.size(ticks) == 2 and (ticks[0] < 0 < ticks[1]):
        ticks = [ticks[0], 0, ticks[1]]
    ticks[0] = max(ticks[0], ext[0])     # apply ..
    ticks[-1] = min(ticks[-1], ext[-1])  # apply saturation to ticks so they don't exceed extents
    sides = dict(x=['top', 'bottom'], y=['right', 'left'])
    for side in sides[xy]:
        if ax.spines[side].get_visible():
            getattr(ax, 'set_' + xy + 'ticks')(ticks)

@applyToAxes
def quick_axis_format(ax, outward=True):
    # does some basic formatting on axis that I feel should be consistent
    for xy in 'xy':
        if outward == True:
            outward_spines(ax=ax, xy=xy)
    set_tick_line_color(ax=ax)
    ax.set_axisbelow(True)
    return ax

@applyToAxes
def format_axis(ax=None, xy='x',
                        ext=None,  # extents of plot area, small buffer added as the graph exceeding is clipped off
                        ticks=None, ticklabels=None,  # specify exact ticks and labels
                        fmt='.1f', app=None, hideslice='',  # tick frmting, append ' s' to last tick for example, hide even or odd ticks with hideslice
                        shorten=1,  # shorten spines to last tick, different options to play with
                        tick_col=grid_color,
                        pos='pad',  # pad has spines outside, hug means they hug chart area (ticks go in), or zero
                        dotsy=False,
                        padright=False,
                        quick=True,  # apply quick axis format first, useful
                        below=True,  # move axes below
                        grid=False,
                        ):  # set x axis at y=0
                        # todo add option to add top or right line?
    ax = ax or mpl.pyplot.gca()
    if quick:
        quick_axis_format(ax, outward=(pos=='pad'))
    if ticks is not None:
        if ticks == 'auto':
            set_auto_tick(ax, xy=xy, ext=ext)
        elif isinstance(ticks, (int, float)):
            ticks = make_ticks(ext, ticks) # if num assume using step with current extents
            getattr(ax, 'set_'+xy+'ticks')(ticks)
        else:
            getattr(ax, 'set_'+xy+'ticks')(ticks)
    else:
        print('pltx.format_axis: WARNING! no ticks passed, expect pboblems')
    if ticklabels:
        getattr(ax, 'set_'+xy+'ticklabels')(ticklabels)
    else:
        fmt_ticks(ax=ax, xy=xy, fmt=fmt, app=app)
    if hideslice:
        hide_ticklabel(ax=ax, xy=xy, slice=hideslice)
    if ext == '0max':
        set_plot_extents(ax=ax, xy=xy, ext=[0, np.max(ticks)])
    elif ext:
        set_plot_extents(ax=ax, xy=xy, ext=ext)
        # set_plot_extents(ax=ax, xy=xy, ext=ext, buff=0.0) # todo testing for semi log
    if shorten:
        shorten_spines(ax=ax, opt=shorten)

    if pos == 'zero':
        zeroed_spine(ax=ax, xy=xy)
    elif pos == 'pad':
        outward_spines(ax=ax, xy=xy)
    elif pos == 'hug':
        hug_spines(ax=ax, xy=xy)

    if dotsy and xy == 'x':
        if not isinstance(dotsy, dict): dotsy = {}
        add_minor_ticks_bottom(ax, **dotsy)
    if padright:
        pad_right_ticks(ax=ax, pad=padright, ticks=ticklabels or ticks, fmt=fmt)
    set_tick_line_color(ax=ax, color=tick_col)  # must be after spines are adjusted

    if grid:
        getattr(ax, xy+'axis').grid(grid)

    ax.set_axisbelow(below)
    ax.set_zorder(9.5)

format_spines_ticks = format_axis


@applyToAxes
def fix_mouse(ax=None):
    ax = ax or mpl.pyplot.gca()
    ax.format_coord = lambda x, y: 'x={:g}, y={:g}'.format(x, y)


@applyToAxes
def add_minor_ticks_bottom(ax=None, num=3, spread=0.1, loc=0.5):
    ax = ax or mpl.pyplot.gca()
    yticks = ax.get_yticks()
    ymin, _ = ax.get_ylim()
    space = np.min(yticks) - ymin
    ymid = ymin + loc*space
    spread = spread*space
    ax.set_yticks(np.linspace(ymid-spread, ymid+spread, num), minor=True)




"""
Text: titles, and labels
"""
@applyToAxes
def set_topright_title(ax=None):
    ax = ax or mpl.pyplot.gca()
    ax.title.set_label_coords(1, 1)  # might wanna use a different metric..?


def rotated_ylabel(ax=None, label='Set label = ""', x=1/2.54, y=0.5/2.54,  right=False):
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
    y_off = y*ratio_default/(xywh[3]*figwh[1])

    if right:
        ax.yaxis.set_label_coords(1-x_off, 1+y_off)  # might wanna use a different metric..
    else:
        ax.yaxis.set_label_coords(-x_off, 1+y_off)  # might wanna use a different metric..
        # todo ensure this is place on top of the axis line





"""
Legends
"""
@applyToAxes
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

@applyToAxes
def set_hist_legend(ax=None):
    # used for histogram
    ax = ax or mpl.pyplot.gca()
    handles, labels = ax.get_legend_handles_labels()
    new_handles = [mpl.lines.Line2D([], [], c=h.get_edgecolor()) for h in handles]
    mpl.pyplot.legend(handles=new_handles, labels=labels)



def legend(*args, **kwargs):
    ax = kwargs.get('ax',  mpl.pyplot.gca())
    #todo need to update dict insteat
    # ncol = 2
    # loc = 'lower right'
    opaque = kwargs.pop('opaque', False)
    kwargs_default = {}
    if opaque:
        kwargs_default = dict(edgecolor='white', facecolor=(1, 1, 1, 1),
                  frameon=True, framealpha=1.0)
    ax.legend(*args,  **kwargs_default, **kwargs)