import matplotlib as mpl

eng = 'lua' # issue with lua only   <<<<<<<<
# eng = 'pdf' # no issue here
# eng = 'xe' # issue here

mpl.use('pgf')
mpl.rc('font', family='serif')
mpl.rcParams.update({
        "pgf.rcfonts"  : False,
        "pgf.texsystem": eng + "latex",
        "pgf.preamble" : '\\usepackage{fontspec}\\usepackage[T1]{fontenc}\\usepackage[utf8x]{inputenc}\\usepackage[light]{kpfonts}',
        # "pgf.preamble" : '\\usepackage[T1]{fontenc}\\usepackage[utf8x]{inputenc}\\usepackage[light]{kpfonts}',
})


import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,6,100)
x = np.sin(t)

fig, ax = plt.subplots()
ax.plot(t, x, label='A line')
plt.title('A function, $f(x) = \sin(x)$, generated with: '+eng)
plt.legend()
plt.savefig('example.pdf')