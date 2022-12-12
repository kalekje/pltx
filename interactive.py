from matplotlib.widgets import Slider, TextBox
import matplotlib.pyplot as plt

"""
todo make more
"""

def _pre_stuff(fig, ax):
    if not fig: fig = plt.gcf()
    if isinstance(ax, (list, tuple)):
        ax = fig.add_axes(ax)
    return ax

def make_textbox(ax, fig=None, kw={}, cb=None, col='black'):
    ax = _pre_stuff(fig, ax)
    tb = TextBox(ax=ax, **kw)
    if cb:
        tb.on_submit(cb)
    if col:
        tb.text_disp.set_color(col)
    return tb, ax

def make_slider(ax, fig=None, kw={}, cb=None, col='black'):
    ax = _pre_stuff(fig, ax)
    sld = Slider(ax=ax, **kw)
    if cb:
        sld.on_changed(cb)
    return sld, ax