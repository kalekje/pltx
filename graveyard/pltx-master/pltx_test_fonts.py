import numpy as np
import matplotlib.pyplot as plt
t = np.linspace(0,6,6000)
y = np.sin(t)

# t, y = crop_xy(t, y, [1,3])


import pltx_fmt
import pltx

eng, font = 'lua', 'sans'
# eng, font = 'lua', 'serif'
# eng, font = 'pdf', 'sans'
# eng, font = 'pdf', 'serif'

pltx.use_pgf(eng=eng, font=font)

fig, ax = plt.subplots()
pltx.set_ax_size_and_pad()
ax.plot(t, y, label='a wave')
plt.title('A function, $f(x) = \sin(x)$')
plt.savefig(eng+'-'+font+'.pdf')

