import matplotlib as mpl


# might want to brighten some of the auxiliary colors
# b r g o y p
#["1400f0", "8b0000", "00820a", "824b00", "788200", "820078"]  ?

grid_color = 'gray'
lightgray = '#BFBFBF'  # 191/255
                    # d8dcd6   (xkcd ???) confirm with latex
blue = "#1000F0"
red = "#B30000"
green = "#00820A"
orange = "#F05F00"
yellow = "#FFC30B"
purple = "#820078"


col_cyc = [blue, red, green, orange, yellow, purple ]
col_cyc_rainbow = [blue, purple, red, orange, yellow, green]

cmap_heat = 'plasma' # gradient colorway for heatmap
cmap_polar = ''  # oposing colorways




def dark_scheme(grid=False):
    thick_line = 1.2
    bg_color = '#222222'
    fg_color = 'white'
    mpl.rcParams['axes.facecolor'] = bg_color
    mpl.rcParams['figure.facecolor'] = bg_color
    mpl.rcParams['savefig.facecolor'] = bg_color
    mpl.rcParams['text.color'] = fg_color  # default text color
    mpl.rcParams['ytick.color'] = fg_color   # changes text AND tick color
    mpl.rcParams['ytick.labelcolor'] = fg_color   # changes text AND tick color
    mpl.rcParams['xtick.color'] = fg_color  # changes text AND tick color
    mpl.rcParams['xtick.labelcolor'] = fg_color  # changes text AND tick color
    mpl.rcParams['axes.labelcolor'] = fg_color # axes label color
    mpl.rcParams['axes.grid'] = grid  # dark scheme implies analysis, grid on
    mpl.rcParams['lines.linewidth'] = thick_line  # in my document, 1.6, 0.8, 0.4 base_font_pt are common thickness,
    mpl.rcParams['axes.spines.top'] = True
    mpl.rcParams['axes.spines.right'] = True
    mpl.rcParams['legend.facecolor'] = 'inherit'
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=  # set color cycle to be brighter than normal
                                                 [adjust_lum(col,1.25) for col in col_cyc])  # todo fix


def adjust_lum(color, amount=0.5):
    # https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    c = list(map(lambda x: min(x,1), c))
    return colorsys.hls_to_rgb(min(c[0],1.0), max(0, min(1, amount * c[1])), c[2])


def use_rainbow():
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=col_cyc_rainbow)


def print_cmap_points(c, n):
    # print_cmap_points('plasma', 12)
    # todo add flip=False
    cmap = mpl.cm.get_cmap(c, n)    # PiYG
    for i in range(0, cmap.N):
        print(mpl.colors.rgb2hex(cmap(i))) # rgb2hex accepts rgb or rgba

