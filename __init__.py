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

def savepdf(name='', fig=None, crop=True, kwargs={}):
    import matplotlib.pyplot as plt
    fig = fig or plt.gcf()
    if crop:
        from pdffun import pdfcrop
        name += '-uncrop'
    fig.savefig(name+'.pdf', **kwargs)
    if crop:
        pdfcrop(name+'.pdf', name.replace('-uncrop','')+'.pdf')

# test
# test new line
# test another
