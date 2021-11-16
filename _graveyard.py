


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

