from .colors import lightgray

# NOTE the sizes are in INCHES, not in ratio of fig like normal mpl convention

ratio_default = 1/1.6 # golden mean approximation, easy to divie up, 1.6 = 8/5

width_default = 4.5  # in inches

subsizes = {
        1: width_default,
        2: 2.0,
        3: 1.25,
}
axsizes = {
        's': subsizes[3],
        'm': subsizes[2],
        'l': width_default,
}

wspace_default = 0.5
hspace_default = 0.5

sspace = dict(
        s=0.25,
        m=0.5,
        l=1,
)


l_default = 1
t_default = 1
b_default = 1

color_main_text = 'black'
grid_color = lightgray

document_font = 11
base_font_pt = document_font - 1

ultra_thick_line = 1.6
very_thick_line = 1.2
thick_line = 0.8
semi_thick_line = 0.6
thin_line = 0.4

tick_length = 4

texeng_default = 'pdf'
font_default = 'sans'


