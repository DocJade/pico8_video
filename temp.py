from math import sqrt

# get closest pixel color to pico-8

# colors by ID, RGB, then name
PicoColors = [
    [0,  0,   0,   0  ], # black
    [1,  29,  43,  83 ], # dark-blue
    [2,  126, 37,  83 ], # dark-purple
    [3,  0,   135, 81 ], # dark-green
    [4,  171, 82,  54 ], # brown
    [5,  95,  87,  79 ], # dark-grey
    [6,  194, 195, 199], # light-grey
    [7,  255, 241, 232], # white
    [8,  255, 0,   77 ], # red
    [9,  255, 163, 0  ], # orange
    [10, 255, 236, 39 ], # yellow
    [11, 0,   228, 54 ], # green
    [12, 41,  173, 255], # blue
    [13, 131, 118, 156], # lavender
    [14, 255, 119, 168], # pink
    [15, 255, 204, 170] # light-peach
]

# https://stackoverflow.com/questions/54242194/
def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in PicoColors:
        id, cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1][0]


# 163:07379:15380:15508: