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
pltx.set_ax_size_and_pad()



ax.plot(t, y, label='a wave')


pltx.format_spines_ticks(xy='x',fmt='.1f',
                         app={1: '\\,s'},
                         ext=[0.2, 4.8],
                         hideslice='',
                         # ticks=0.5*np.arange(2, 5),
                         ticks=[0.2, np.pi/4, 2],  # testing ticks==extents, see if they touch
                         ticklabels=['0.2', '$\pi/4$', 2.0],
                         shorten=1
                         )
pltx.format_spines_ticks(xy='y',
                         # ticks=0.5*np.arange(-2, 3),
                         ext=[-1, 1],
                         # ext=[-0.9, 0.9],
                         ticks=[-1.0, -0.5, 0.0, 0.5, np.sqrt(1/2), 1.0],
                         ticklabels=['-1.0', '', '0.0', '', '', '1.0\\,kV'],
                         # ticks=[-0.5, 0.0, 0.5],
                         # ticklabels=['bot', 'mid', 'top'],
                         # hideslice='e',
                         # fmt='.1f',
                         # app={-1:'\\,kV'},
                         shorten=1,
                         )

ax.set_yticks([-0.75, -0.25, 0.25, 0.75], minor=True)  # smaller ticks, typically only used in log plot
# must also set color

pltx.add_right_yaxis(ax, shorten=1,
                     ticks=[0, -0.5, -np.sqrt(0.5), np.sqrt(0.5)],
                     ticklabels=['', '', r'$-\sqrt{2}/2$', r'$\sqrt{2}/2$']
                     )
pltx.add_top_xaxis(ax)
# pltx.draw_line(x=[0,4], y=[0.5,0.5])
# pltx.draw_line(x=[0,4], y=[1,1])

# ax.add_line(mpl.lines.Line2D(x, y, lw=thin_line, color=color, alpha=1.0, clip_on=True, transform=ax.transAxes))

# pltx.add_gridline(-0.5,  d='h')
# pltx.add_gridline(0.0,  d='h')
# pltx.add_gridline(1.0)

pltx.add_callout(ax=ax, loc=[np.pi/4,np.sqrt(2)/2])

pltx.rotated_ylabel('Amplitude', ax=ax, x=0, y=0.0)
# plt.xlabel('Time, s')

# ax.spines['right'].set_visible(True)
# ax.spines['right'].set_position(('axes',1.0))  # todo must add option for additional axis and ticks
ax.legend()
plt.savefig('fig.pdf')