"""
pltx -- matPLoTlib eXtras
Some useful functions to make my plots consistent and report-ready.
"""

from . import rcParas
from .colors import dark_scheme, adjust_lum, use_rainbow
from .sizing import *
from .format import *
from .interactive import *
from .tex import use_tex, sublet
from .multipageplot import *
from . import plasmax

def showmax():
    import matplotlib.pyplot as plt
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    # mng.resize(*mng.window.maxsize())
    plt.show()

# test new line
# test another
