import matplotlib as mpl
from .defaults import ratio_default, width_default, subsizes, axsizes, wspace_default, hspace_default, l_default, t_default, b_default, sspace
# from .defaults import wspace_small, hspace_medium, hspace_large
# todo nail down tlrb spacing

# Figures and Axes sizing

def get_axes_size(fig=None):
    # get 1x1 axes size in inches based on figure and rltb padding
    if fig is None: fig = mpl.pyplot.gcf()
    figw, figh = fig.get_size_inches()
    axw = figw*(fig.subplotpars.right-fig.subplotpars.left)
    axh = figh*(fig.subplotpars.top-fig.subplotpars.bottom)
    return axw, axh

def set_ax_size_and_pad(fig=None, w=width_default, h=None,
    l=l_default, t=t_default, r=None, b=b_default, square=False):
    # creates a fig size and layout format based on desired axes size and padding, better for consistent ax size
    # all units are inches
    fig = fig or mpl.pyplot.gcf()

    if isinstance(w, str):
        w = axsizes[w]

    h = h or w *(1 if square else ratio_default)

    r = r or l + 0.000001  # equal left and right padding

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
    return fig

def set_subp_pad(fig=None, rows=None, cols=None, ws=wspace_default, hs=hspace_default):
    # set the hspace and space parameter in inches
    fig = fig or mpl.pyplot.gcf()
    Wax, Hax = get_axes_size(fig)
    fig.subplots_adjust(hspace=rows/(Hax/hs + 1 - rows),
                        wspace=cols/(Wax/ws + 1 - cols))
    return fig



def set_subp_size_and_fig(fig=None, rows=None, cols=None, W=None, H=None,
                           h=1, w=1/1.6, l=1.5, r=1.5, t=1.5, b=1.5):
    # set a subplots individual axis size, padding, hspace and wspace all in inches
    fig = fig or mpl.pyplot.gcf()
    rows = rows or fig.axes[0].numRows
    cols = cols or fig.axes[0].numCols
    if not any([W, H]):
        figw, figh = fig.get_size_inches()
    else:
        fig.set_size_inches(W, H)

    kwargs = {
        'left' : l/figw,
        'right' : 1 - r/figw,
        'top' : 1-t/figh,
        'bottom': b/figh,
        'hspace': 1-h/(figh - t - b)*(rows-1), #l/figw/(rows-1),
        'wspace': 1-w/(figw - l - r)*(cols-1) #l/figw/(rows-1),
    }

    fig.subplots_adjust(**kwargs)
    return fig

def set_subp_size_and_pad(fig=None, rows=None, cols=None,
                          w=None, h=None, ss=None, hs=hspace_default, ws=wspace_default,
                          l=l_default, t=t_default, r=None, b=b_default, square=False):
    # set a subplots individual axis size, padding, hspace and wspace all in inches
    fig = fig or mpl.pyplot.gcf()

    rows = rows or fig.axes[0].numRows
    cols = cols or fig.axes[0].numCols

    w = w or subsizes[cols]
    if isinstance(w, str):
        w = axsizes[w]
    h = h or w *(1 if square else ratio_default)
    r = r or l + 0.000001  # equal left and right padding
    if ss == 0: ss = 0.00001
    if ss: # subplot space for both
        if isinstance(ss, str):
            ss = sspace[ss]
        hs, ws = ss, ss
    else:
        if isinstance(hs, str):
            hs = sspace[hs]
        if isinstance(ws, str):
            ws = sspace[ws]

    ax_width = cols*w + (cols-1)*hs
    ax_height = rows*h + (rows-1)*hs
    fig = set_ax_size_and_pad(fig=fig, w=ax_width, h=ax_height, l=l, t=t, r=r, b=b)
    fig = set_subp_pad(fig=fig,rows=rows,cols=cols,ws=ws,hs=hs)
    return fig

def makeplots(nrows=1, ncols=1, squeeze=False, square=False, subplots_args={}, size={}):
    # only squeeze for 1x1, don't squeeze otherwise
    if square: size.update({'square' : square})
    if nrows * ncols == 1:
        squeeze = True
    fig, axs = mpl.pyplot.subplots(nrows=nrows,ncols=ncols,squeeze=squeeze,**subplots_args)
    if nrows * ncols == 1:
        set_ax_size_and_pad(ax=axs, **size)
    else:
        set_subp_size_and_pad(fig=fig, **size)
    return fig, axs
