

# https://matplotlib.org/3.4.3/gallery/ticks_and_spines/spines_bounds.html


import numpy as np
import functools as ft, operator as op

# https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties
def rgetattr(obj, attr, *args):  # recursive getattr, works for nested attr
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return ft.reduce(_getattr, [obj] + attr.split('.'))


def is_arr(o):
    return isinstance(o, (list, tuple, np.ndarray))





