import pltx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

pltx.use_pgf()
# pltx.dark_scheme(grid=True)


cols = {}
cols['lg'] = '#BFBFBF'





t = np.linspace(0,6,6000)
y = np.sin(t*16)

# t, y = crop_xy(t, y, [1,3])

fig, ax = plt.subplots()
ax.plot(t, y, label='a wave')


pltx.box_zoom(ax)

# plt.title('\\bfseries My title')
pltx.shorten_spines()

# plt.margins(x=0,y=0)
# ax.spines['bottom'].set_position(('data', 0))
# ax.spines['bottom'].set_position('zero')
# todo probably want width for right side axes
# plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
# plt.gca().tick_params(which='x', color=cols['lg'], lw=0.4) # todo set minor
# plt.margins(0.1,0.1)

pltx.fmt_ticks(xy='y',fmt='.1f')
pltx.fmt_ticks(xy='x',fmt='.1f',app={6: ' s'})
pltx.hide_ticklabel(xy='y', slice='e')  # must come after formatting
pltx.hide_ticklabel(xy='x', slice='o')
ticks = plt.gca().get_xticks()
labs = plt.gca().get_xticklabels()
# pltx.fmt_ticks(xy='x',fmt='.2f',app={-1: ' s', 0: ' s', 1: ' s'})
# format, hide, then line color
pltx.set_tick_line_color() # must be after spines are adjusted
# todo fix conflict between hiding labels and formatting, there is an issue
pltx.rotated_ylabel('Amplitude, kV')
# plt.xlabel('Time, s')
plt.legend()
plt.savefig('fig.pdf')