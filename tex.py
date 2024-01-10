
import matplotlib as mpl
from .defaults import tex_preamble_default


preambles = {}

#language=tex
preambles['kp serif pdf'] = r"""
\usepackage[utf8x]{inputenc}
\usepackage[light]{kpfonts}
"""

#language=tex
preambles['kp serif lua'] = r"""
\usepackage{fontspec}
\usepackage[T1]{fontenc}
""" + preambles['kp serif pdf']

#language=tex
preamble_cmbright = r"""
\usepackage[T1]{fontenc}
\usepackage{cmbright}
\let\CMserif\rmdefault
\renewcommand\bfdefault{sb}
\newcommand\sbdefault{bx}
"""

#language=tex
preambles['cmb sans pdf'] = r"""
\usepackage[utf8x]{inputenc}
""" + preamble_cmbright

#language=tex
preambles['cmbold sans lua'] = r"""  
\usepackage[utf8x]{inputenc}
\usepackage{fontspec}
""" + preamble_cmbright



#language=tex
preambles['cmb sans lua'] = r"""
\usepackage{fontspec}

\setsansfont{cmunb}[
    Extension=.otf,
    UprightFont=*mr,
    ItalicFont=*mo,
    BoldFont=*sr,
    BoldItalicFont=*so,
    NFSSFamily=cmbr
    ]

\usepackage{cmbright}  % hello
\gdef\bfdefault{sb}
\gdef\sbdefault{bx}    

\setmonofont{CMU Typewriter Text Light}

\DeclareSymbolFont{iwonalargesymbols}{OMX}{iwona}{m}{n}
\DeclareMathSymbol{\intop}{\mathop}{iwonalargesymbols}{"52}
"""


#language=tex
preambles['calibri sans lua'] = r"""
\usepackage{fontspec}


\setmainfont{calibri}
\setsansfont{calibri}

% https://tex.stackexchange.com/questions/439998/math-in-ms-calibri

\usepackage[math-style=upright]{unicode-math}
\usepackage{mathtools}

\setmathfont[slash-delimiter=frac]{Cambria Math}
\setmathfont[range=up]{Calibri}
\setmathfont[range=it]{Calibri Italic}
\setmathfont[range=bfup]{Calibri Bold}
\setmathfont[range=bfit]{Calibri Bold Italic}

\setoperatorfont\normalfont % For log, sin, cos, etc.
"""


#language=tex
common_preamble = r"""
\usepackage{amsmath}
\usepackage{xfrac}
\usepackage{siunitx}
"""

import re
def clean_preamble(preamble):
    preamble = re.sub('%.*\n', ' ', preamble) # clear comments
    return preamble.replace('\n',' ')  # ensure comments are removed # todo do a regex replace to remove all comments from latex file???


def use_tex(preamble=tex_preamble_default, font='sans', eng='lua'):  # to enable latex text formatting
    if any([preamble.strip().endswith('.' + x) for x in ['sty', 'tex', 'txt']]):  # if a file is given
        with open(preamble) as file:
            preamble = file.read()
            # if preamble file is passed, so must font and eng
    else:  # otherwise take from preambles dictionary, keys are formatting like so: '<name> <sans or serif> <tex engine>'
        font, eng = preamble.split()[1:]
        preamble = preambles[preamble] + common_preamble

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
