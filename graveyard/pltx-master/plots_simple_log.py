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
y = np.exp(t)*(np.sin(t*16)**2)
t = t[20:] # remove 0
y = y[20:] # remove 0
# t, y = crop_xy(t, y, [1,3])

fig, ax = plt.subplots()
pltx.set_ax_size_and_pad()

ax.semilogy(t, y, label='a wave')  # todo investigate semi-log



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
                         # ext=[-1, 1],
                         # ext=[-0.9, 0.9],
                         # ticks=[-1.0, -0.5, 0.0, 0.5, np.sqrt(1/2), 1.0],
                         # ticklabels=['-1.0', '', '0.0', '', '', '1.0\\,kV'],
                         # ticks=[-0.5, 0.0, 0.5],
                         # ticklabels=['bot', 'mid', 'top'],
                         # hideslice='e',
                         # fmt='.1f',
                         # app={-1:'\\,kV'},
                         ext=[0.001, 100],  # todo why arent extents playign nice with semi log?
                         shorten=2,
                         )


# pltx.add_right_yaxis(ax, shorten=1,
#                      ticks=[0, -0.5, -np.sqrt(0.5), np.sqrt(0.5)],
#                      ticklabels=['', '', r'$-\sqrt{2}/2$', r'$\sqrt{2}/2$']
#                      )


# pltx.add_callout(ax=ax, loc=[np.pi/4,np.sqrt(2)/2])
pltx.add_callout(ax=ax, loc=[4,9], log='y')  # todo, this sets axis value on linear scale, must be log

pltx.rotated_ylabel('Amplitude', ax=ax, x=0, y=0.0)

ax.legend()
plt.savefig('figsemilog.pdf')
