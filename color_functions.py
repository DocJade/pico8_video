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

# Quantize the image https://stackoverflow.com/questions/5906693/
def kmeans_color_quantization(image, clusters=8, rounds=1):
   h, w = image.shape[:2]
   samples = np.zeros([h*w,3], dtype=np.float32)
   count = 0
   for x in range(h):
      for y in range(w):
         samples[count] = image[x][y]
         count += 1
   compactness, labels, centers = cv2.kmeans(samples,
         clusters, 
         None,
         (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
         rounds, 
         cv2.KMEANS_RANDOM_CENTERS)
   centers = np.uint8(centers)
   res = centers[labels.flatten()]
   return res.reshape((image.shape))