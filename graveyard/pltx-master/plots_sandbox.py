import numpy as np
import matplotlib.pyplot as plt

import pltExtras_defaults
import pltExtras_new as pltx

t = np.linspace(0,6,100)
y = np.sin(t)


fig, ax = plt.subplots()
# ax.plot(t, y, label='hello')
# ax.hist2d(t, y)
ax.hexbin(t, y)
ax.set_title('yolo')
ax.set_xlabel('yolo')
ax.margins(x=0,y=0)
# todo remove spine
# ax.set_xmargin(0) # what's the difference?, below doesnt work, top does
# ax.set_ymargin(0)
pltx.set_tick_line_color(ax, 'white')
fig.savefig('fig.pdf')