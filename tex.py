
import matplotlib as mpl
from .defaults import texeng_default, font_default


default = {}

#language=tex
default['pdf-serif'] = r"""
\usepackage[utf8x]{inputenc}
\usepackage[light]{kpfonts}
"""

#language=tex
default['lua-serif'] = r"""
\usepackage{fontspec}
\usepackage[T1]{fontenc}
""" + default['pdf-serif']

#language=tex
preamble_cmbright = r"""
\usepackage[T1]{fontenc}
\usepackage{cmbright}
\let\CMserif\rmdefault
\renewcommand\bfdefault{sb}
\newcommand\sbdefault{bx}
"""

#language=tex
default['pdf-sans'] = r"""
\usepackage[utf8x]{inputenc}
""" + preamble_cmbright

#language=tex
default['lua-sans'] = r"""
\usepackage[utf8x]{inputenc}
\usepackage{fontspec}
""" + preamble_cmbright

#language=tex
common = r"""
\usepackage{amsmath}
\usepackage{xfrac}
\usepackage{siunitx}
"""

import re
def clean_preamble(preamble):
    return preamble.replace('\n',' ')  # ensure comments are removed # todo do a regex replace to remove all comments from latex file???


def use_tex(preamble='', font=font_default, eng=texeng_default):  # to enable latex text formatting
    if any([preamble.strip().endswith('.' + x) for x in ['sty', 'tex', 'txt']]):
        with open(preamble) as file:
            preamble = file.read()
    elif preamble:
        pass # todo custom preambe
    else:
        preamble = default[eng + '-' + font] + common
    preamble = clean_preamble(preamble)
    mpl.rc('font', family=(font == 'sans')*'sans-' + 'serif')  # set non-math font correctly
    mpl.use('pgf')
    mpl.rcParams.update({
            "pgf.rcfonts"  : False,
            "pgf.texsystem": eng + "latex",
            "pgf.preamble" : preamble,
    })


def sublet(n): # subplot number to letter
    return r'\textbf{('+chr(97+n)+')} \,'

# add other functions later
