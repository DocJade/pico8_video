#DocJade

#functions that have stuff to do with colors.

import pico_specs
from math import sqrt

# https://stackoverflow.com/questions/54242194/

# This function loops over the pico colors, and finds the
# nearest color to the given RGB value.

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in pico_specs.PICO_COLORS:
        id, cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1][0]
