import pltx
pltx.use_tex()
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2)
pltx.set_subp_size_and_pad(fig,w=4,h=4,hs=1)
axs[0].plot([-1,0,1],[-1,0,1])
axs[1].plot([-1,0,1],[-1,0,2])
# pltx.format_axis(fig, xy='y', ext=[0,2], ticks='auto')
pltx.format_axis(axs, xy='y', ext=[-1,2], ticks=0.5, hideslice='o', pos='zero')
pltx.format_axis(axs, xy='x', ext=[-1,1], ticks=0.25, fmt='.2f',    pos='zero')

pltx.savepdf('test')

