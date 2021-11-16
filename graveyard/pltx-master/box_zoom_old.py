


def get_data_extents(ax=None):
    # todo consider making this general so it might work with hexbin plot or histogram, for example
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



def box_zoom(ax=None, x=None, y=None,
             xm=0.05/1.6, ym=0.05):
    ax = ax or mpl.pyplot.gca()

    for l in ax.get_lines():
        x_dat, y_dat = l.get_xdata(), l.get_ydata()
        if x:
            del_x = (x_dat <= x[0]) | (x_dat >= x[1])
            # todo: option to linearly interpolate end point to extent
            x_dat[del_x] = np.nan
            y_dat[del_x] = np.nan
        if y:
            del_y = (y_dat <= y[0]) | (y_dat >= y[1])
            # todo: option to linearly interpolate end point to extent
            x_dat[del_y] = np.nan
            y_dat[del_y] = np.nan
        l.set_ydata(y_dat)
        l.set_xdata(x_dat)
    if (not x) or (not y):
        x_min, x_max, y_min, y_max = get_data_extents(ax=ax)
    if x:
        x_min, x_max = x
    if y:
        y_min, y_max = y
    set_plot_marg(ax=ax, x=[x_min, x_max], y=[y_min, y_max], xm=xm, ym=ym)


def set_plot_marg(ax=None, x=None, y=None, xm=0.05/1.6, ym=0.05):
    ax = ax or mpl.pyplot.gca()
    if x:
        x_min, x_max = x
        x_buff = xm*(x_max - x_min)
        ax.set_xlim(x_min - x_buff, x_max)
    if y:
        y_min, y_max = y
        y_buff = ym*(y_max - y_min)
        ax.set_ylim(y_min - y_buff, y_max + 0.01*(y_max - y_min))

def make_ticks(ext, step):
    # makes a np range between two nubers with appropriate step
    return np.arange(ext[0], ext[1]*(1+0.0001), step)


def try_float(x):
    try:
        return float(x)
    except:
        return x









import pltx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)





t = np.linspace(0,6.30,20)
f = np.sin(t)

y = [-0.8, 0.8]

del_y = (f <= y[0]) | (f >= y[1])
# todo: option to linearly interpolate end point to extent

del_y_shift = np.roll(del_y, -1)
del_y_shift[-1] = False
trans = del_y != del_y_shift
t_new = t
f_new = f
t_new[del_y] = np.nan
f_new[del_y] = np.nan

###
# NOTE this could be achieved by doing a for loop and interpolating points of going to outside the limit to inside,
# or coming from outside limit to coming inside. Woudl require changing data. New solution: adjust spines!
##

for i in np.where(trans)[0]:
    if del_y[i]:
        if f[i] > y[1]:
            f_new[i+1] = f_new  # todo detect above or below
            t_new[i+1] = t[i]
        elif f[i] > y[1]:
            f_new[i + 1] = f_new  # todo detect above or below
            t_new[i + 1] = t[i]
    else:
        pass

# The problem to solve:
# applying the np.nan can chop off the signal
# I would like to replace the chopped part with a point
# that fits in the boundary so the signal looks a bit better
# required "replacing" the chopped (x,y) point in both arrays
# with one that fits in our chart area



fig, ax = plt.subplots()
ax.plot(t, f, label='a wave')
plt.show()




import pltx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)





t = np.linspace(0,6.30,20)
f = np.sin(t)

y = [-0.8, 0.8]
x = [0.5, 7.5]

fig, ax = plt.subplots()
ax.plot(t, f, label='a wave')
ax.set_ylim(*y)
ax.set_xlim(*x)
# ax.spines.left.set_position(('axes', 0.6))
# ax.set_clip_on(False)
ax.spines['bottom'].set_position(('axes', -0.05))
ax.spines['left'].set_position(('axes', -0.05))
# plt.show()
plt.savefig('test.pdf')