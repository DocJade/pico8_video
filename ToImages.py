import cv2
from math import sqrt
import numpy as np

# get closest pixel color to pico-8
# colors by ID, RGB, then name
PicoColors = [
    ["00",  0,   0,   0  ], # black
    ["01",  29,  43,  83 ], # dark-blue
    ["02",  126, 37,  83 ], # dark-purple
    ["03",  0,   135, 81 ], # dark-green
    ["04",  171, 82,  54 ], # brown
    ["05",  95,  87,  79 ], # dark-grey
    ["06",  194, 195, 199], # light-grey
    ["07",  255, 241, 232], # white
    ["08",  255, 0,   77 ], # red
    ["09",  255, 163, 0  ], # orange
    ["10", 255, 236, 39 ], # yellow
    ["11", 0,   228, 54 ], # green
    ["12", 41,  173, 255], # blue
    ["13", 131, 118, 156], # lavender
    ["14", 255, 119, 168], # pink
    ["15", 255, 204, 170] # light-peach
]
PicoColorsGS = [
    ["00",  0,   0,   0  ], # black
    #["01",  29,  43,  83 ], # dark-blue
    #["02",  126, 37,  83 ], # dark-purple
    #["03",  0,   135, 81 ], # dark-green
    #["04",  171, 82,  54 ], # brown
    ["05",  95,  87,  79 ], # dark-grey
    ["06",  194, 195, 199], # light-grey
    ["07",  255, 241, 232], # white
    #["08",  255, 0,   77 ], # red
    #["09",  255, 163, 0  ], # orange
    #["10", 255, 236, 39 ], # yellow
    #["11", 0,   228, 54 ], # green
    #["12", 41,  173, 255], # blue
    #["13", 131, 118, 156], # lavender
    #["14", 255, 119, 168], # pink
    #["15", 255, 204, 170] # light-peach
]
ModifiedPal = [
    ["00",  0,   0,   0  ], # black
    ["01",  29,  43,  83 ], # dark-blue
    ["02",  126, 37,  83 ], # dark-purple
    ["03",  0,   135, 81 ], # dark-green
    ["04",  171, 82,  54 ], # brown
    ["05",  95,  87,  79 ], # dark-grey
    ["06",  159, 170, 180], # light-grey
    ["07",  215, 223, 227], # white
    ["08",  255, 0,   77 ], # red
    ["09",  255, 163, 0  ], # orange
    ["10", 255, 200, 72 ], # yellow
    ["11", 0,   228, 54 ], # green
    ["12", 78,  197, 207], # blue
    #["13", 131, 118, 156], # lavender
    ["14", 236, 105, 113], # pink
    ["15", 243, 203, 180] # light-peach
]

# https://stackoverflow.com/questions/54242194/
def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in PicoColors: # switch palette here
        id, cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1][0]

def rle(input: str):
   # var setup
   current_run = -1
   current_color = False # assume black start.
   rle_array = []
   print("RLE: Counting... ", end='')
   for i in input:
      if i != current_color:
         # end of run!
         rle_array.append(current_run + 1)
         current_run = 0
         # flip the color
         current_color = not current_color
         continue
      else:
         # color is the same, increment run.
         current_run += 1
         continue

   # done counting.
   print("Done!")
   
   # now we will construct the rle string
   print("RLE: Building string... ", end='')

   output_string = ""
   for i in rle_array:
      output_string += (str(i) + ",")

   print("Done!")

   return output_string

def string_rle(input: str, step: int):
   # var setup
   current_run = 1
   current_color = input[0:step] # get first color
   input = input [step:] # remove first 2
   rle_array = []
   print("RLE: Counting... ", end='')
   # https://stackoverflow.com/questions/43428
   def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
   
   for i in chunker(input, step):
      if i != current_color:
         # end of run!
         rle_array.append(current_color + "," + str(current_run + 1))
         current_run = 0
         # flip the color
         current_color = i
         continue
      else:
         # color is the same, increment run.
         current_run += 1
         continue

   # done counting.
   print("Done!")
   
   # now we will construct the rle string
   print("RLE: Building string... ", end='')

   output_string = ""
   for i in rle_array:
      output_string += (str(i) + "/")

   print("Done!")

   return output_string


# compression function
def basic_rle(frame: list):
   """rle format:
   [         - begin frame
   first bit - background color.
   :##       - swap color for this many pixels
   >##       - skip forward this many pixels
   ]         - end frame
   """
   # expected output for a full screen of white:
   # [1]

   # expected output for a screen of white with one pixel of black at first position
   # [1:1]

   # expected output for a screen of white with a black pixel at the 32 position
   # [1>31:1]

   
   #we want to count the number of each color to set the background color, init those vars here
   num_dark = 0
   num_light = 0
   bg_color = 0
   
   # make array for storing wip RLE
   RLE_temp_array = [] # this will be an array of strings

   # now we will start counting!
   # setup vars
   index = 0
   current_run = -1
   current_color = frame[0]
   while index < len(frame):
      # bg color counting
      if frame[index] == 0:
         #dark
         num_dark += 1
      else:
         num_light += 1
      
      if frame[index] != current_color:
         # changed color!
         # add run length to rle temp
         current_run += 1
         RLE_temp_array.append(current_run)
         # reset vars
         current_run = 0
         current_color = frame[index]
      else:
         # color is the same, increment run.
         current_run += 1
      index += 1
   
   # done looping, now we need to assemble the string.
   output_string = "["

   # determine background color
   if num_light >= num_dark:
      # use white background
      bg_color = 1
   else:
      # black background
      bg_color = 0

   output_string += str(0 if bg_color == 1 else 0) # needs to be inverted for some reason?

   # now we need to loop over the returned runs

   rle_index = 0
   rle_color = frame[0] # first color, will be flipped every time the index is advanced

   # early return if the there is nothing to process
   if len(RLE_temp_array) == 0:
      # early return!
      output_string += "]"
      return output_string

   while rle_index < len(RLE_temp_array):
      #check if this is a skip or a coloring in
      if bg_color == rle_color:
         # same as bg color, this is a skip.
         output_string += (">" + str(RLE_temp_array[rle_index]))
      else:
         # not the same color, this is a fill.
         output_string += (":" + str(RLE_temp_array[rle_index]))
      # flip color
      rle_color = 1 if rle_color == 0 else 0
      # increment
      rle_index += 1
   

   # all done! cap the frame and return!
   output_string += "]"
   return output_string



def frame_compress(full_video: str):
   """
   Background color is always white, as there is less
   black pixels to store than white ones

   We are running the RLE on the entire video for
   maximum possible run lengths.

   first pixel is assumed to be black, because that is true
   for bad apple.

   We aren't storing any information about where the frames begin or end,
   that is a job for the decompression.
   since frames are a static size, its easy for the decompression to
   automatically chop up the output.
   """

   # the first step of compression is easy, just loop until we find a change
   # then store how long the runs are.
   current_run = 0
   runs = []
   current_color = 0 # assumed black
   print("Iterating pixels. Please wait... ",end="") # no newline.
   for i in full_video:
      if int(i) != current_color:
         # color has changed!
         # save the run
         runs.append(current_run)
         # reset run counter
         current_run = 1 # we are on the first pixel of the new run
         current_color = int(i)
         continue
      else:
         # same color.
         current_run += 1
         continue

   print("Done!")
   
   """
   Now that we have all of the runs, we need to turn all
   of the runs into a big string, separated by ,'s

   this means that commas mark the end/switch of a run
   """
   full = ""
   for i in runs:
      full += (str(i) + ",")
#TODO finish this? idea is kinda killed bc of int>char>int>bin missing.


def xor_comp(full_video: str):
   bits_per_frame = (128*96)
   # first frame is solid black.
   prev_frame = "0"*bits_per_frame
   output = ""
   # loop over each frame
   for frame in range(1, 6571*bits_per_frame, bits_per_frame):
      cur_frame = full_video[i:i+bits_per_frame]
      # xor that sucker
      xor_ed = int(str(prev_frame), 2)^int(str(cur_frame), 2)
      xor_str = bin(xor_ed)[2:].zfill(len(cur_frame))
      # turn to string and append to output.
      output += xor_str
      # move current frame into prev
      prev_frame = frame
      continue # next!

   # now we can RLE the XOR output then
   # write out to file.
   with open("RLE_XOR_Output.txt", "w") as text_file:
      print(rle(output), file=text_file)

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

def color_comp():
   # we are going to do all the video handling here, since
   # this is so different from the rest of the b&w functions

   #load the video
   
   print("Loading video... ",end='')
   SourceVideo = cv2.VideoCapture('OhMyGah_discord.mp4')
   frame_count = int(SourceVideo.get(cv2.CAP_PROP_FRAME_COUNT))
   count = 0
   success = True
   print("Done!")
   
   # now we will loop over each frame of the video, 
   # resize the video to pico-8 size, then appending to
   # the array with the color of each pixel value

   print("Begin iterating frames...")
   FrameColorArray = []
   while count < frame_count:
      print("Frame " + str(count) + "... ",end="")

      # open the image from the frame

      success,image = SourceVideo.read()

      # up the saturation

      image = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)

      #multiple by a factor to change the saturation
      #https://answers.opencv.org/question/193336/

      image[...,1] = image[...,1]*1.4

      image=cv2.cvtColor(image,cv2.COLOR_HSV2RGB)

      # denoise the image SLOW!
      # image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
      # Quantize the image SLOW! # There are only 16 colors in the pico pallet, so no need to
      # quantize for more than that.
      # results in high flicker.
      # image = kmeans_color_quantization(image, clusters=16,rounds=1)
      # Bilateral Filtering # not too slow, still chroma noisy
      image = cv2.bilateralFilter(image,18,800,800)
      # Median color
      # image = cv2.medianBlur(image,9)
      # Gaussian blur
      # image = cv2.GaussianBlur(image,(9,9),0)

      # now resize the image. since this is
      # anime / line art, use INTER_CUBIC.

      image = cv2.resize(image, (128,96), interpolation = cv2.INTER_CUBIC)

      # save image as bmp for QA

      cv2.imwrite("output/frame%d.bmp" % count, image)

      # loop over pixels

      for i in range(96):
        for j in range(128):
            current_pixel = image[i,j] # this is an rgb value,
            FrameColorArray.append(current_pixel) # put the color into the array
      
      # done looping over the pixels!
      count += 1
      print("Done!")

   # done looping over frames!
   print("Done iterating frames!")

   # now we need to process the colors in the array to find the nearest pico-8 color 

   PicoReadyColors = []
   print("Finding closest colors.")
   print("Please wait, This will take a while.")
   for i in FrameColorArray:
      PicoReadyColors += closest_color(i)

   print("Done!")
   print(len(PicoReadyColors))

   # write the colors to file
   with open("Pico_Colors.txt", "w") as text_file:
    print(PicoReadyColors, file=text_file)

   # now that we have the closest colors, we shall construct the initial frame of the video.
   # we are going to dump the colors straight into a string, since the colors are padded to
   # 2 digits, it will be easy to deconstruct later.

   print("Building initial frame...")
   InitialFrame = ""
   for _ in range((128*96)):
      InitialFrame += PicoReadyColors.pop(0)
      InitialFrame += PicoReadyColors.pop(0)
   
   # now throw that string into RLE for better compression.
   # Osaka's forehead has a lot of duplicate colors after all.

   print("Running RLE...")
   InitialFrame_RLE = string_rle(InitialFrame,2)

   # now output the rle!
   # Save the output to First_Frame
   with open("First_Frame.txt", "w") as text_file:
    print(InitialFrame_RLE, file=text_file)
   print("Done!")

   # now that the original frame is done, we can start comparing subsequent frames
   # to find the differences.

   CurrentFrame = InitialFrame
   
   # Loop to grab frames and compare until we run out of pixels.
   FinalCompressed = ""

   print("Starting change based compression!")

   while len(PicoReadyColors) > 0:
      # Still got a frame worth of pixels, lets get to work.

      # The format for the frames that are compared to previous frames works as follows:
      # A number that indicates how far into the frame the changed pixel is.
      # The new color of the pixel.
      # Marker for end of frame.

      # Example: 0:00>
      # Change pixel `0` to color `00`, end of frame.

      # If no changes are present, the entire frame will be expressed as `>`.
      # Runs are not accounted for, every pixel gets its own entry.
      # There is no need to store the beginning and end of pixels, since the size of the color
      # is always 2 digits.

      # Example: 234:10123:05>
      # We take the entire string and split on :
      # 234 10123 05>
      # the first number in the frame is always an offset, so now we know to move
      # `234` pixels forwards, so we move, then discard.
      # 10123 05>
      # now we need the color of the pixel we just shifted over to, so we "pop" the first
      # 2 numbers in the next string
      # "10" 123 05>
      # we set the color of the pixel, then repeat.
      # 123 05>
      # 05>
      # >
      # When we hit the end of the frame, we will have 0 items left in the list, since
      # the string provided to the function has already had the `>` removed.
      # Example:
      # 234:121:01>12:0132:15>
      # 234:121:01 12:0132:15 "" # not sure if the final item will be empty, need to check.
      # 234:121:01
      # 234 121 01
      # 121 01
      # 1 01
      # 01
      # ""

      # SPEC UPDATE:
      # Now storing offsets from previous index.
      # 123, 124 is now 123,1

      # Now lets get to work!
      NextFrame = ""
      CondensedFrame = ""
      CurrentOffset = 0


      # grab the next frame.
      NextFrame = PicoReadyColors[:((128*96)*2)] # steal next frame
      PicoReadyColors = PicoReadyColors[((128*96)*2):] # drop stolen frame

      #for _ in range((128*96)):
      #   NextFrame += PicoReadyColors.pop(0)
      #   NextFrame += PicoReadyColors.pop(0)

      # Now loop over both frames, storing the differences immediately into the final string.
      
      for i in range(0, (128*96)*2, 2):
         # 0 is the top left pixel.
         if (CurrentFrame[i] == NextFrame[i]) and (NextFrame[i+1] == CurrentFrame[i+1]): # 2 conditions for short circuiting.
            # Same, Skip.
            continue
         else:
            # New color! Store the i and color
            print(".", end='') # print a dot for every hit.
            # Since the array of colors in the frame are 2 digits per pixel, we need to half i.
            CondensedFrame += str(int(i/2) - CurrentOffset)
            CondensedFrame += ":"
            CondensedFrame += str(NextFrame[i])
            CondensedFrame += str(NextFrame[i+1]) # could probably use .. here.
            CurrentOffset = int(i/2)
            # cool! NEXT!
            continue

      # We've finished looping over every pixel.
      # Now we will cap the frame, and add it to the final output.
      # But first! if we only changed one pixel, we dont really care.
      if CondensedFrame.count(":") == 1:
         # only one change, discard.
         CondensedFrame = ""
         # print a bang to signify the discard'
         print("!", end='')

      print(">\n") # done with frame, cap the debug output.
      FinalCompressed += CondensedFrame + ">"
      # What's new is old.
      CurrentFrame = NextFrame
      # Next frame!
      continue

   # We've done every frame!
   # Save the output to Gah_Changes
   with open("Gah_Changes.txt", "w") as text_file:
    print(FinalCompressed, file=text_file)
   print("Done!")
      

"""
vidcap = cv2.VideoCapture('BadAppleSource.mp4')
success,image = vidcap.read()
frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
count = 0
success = True
full_output = ""
while count < 6572:
  # skip every third frame to drop framerate to 30fps
  if count % 3 == 0 and count != 0:
     print("skip!")
     count += 1
     continue
  
  print("Frame " + str(count) + "...")
  success,image = vidcap.read()
  # now we resize the image
  image = cv2.resize(image, (128,96), interpolation = cv2.INTER_CUBIC)
  # apply the threshold
  ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
  # save image as bmp
  #cv2.imwrite("output/frame%d.bmp" % count, image)
  # loop over pixels and get the frame's bits
  frame_bits = "" # we store all the bits for the frame here
  for i in range(96):
    for j in range(128):
        current_pixel = image[i,j] # this is an rgb value, we only care about brightness
        bit = (current_pixel[0] == 0) # white is true
        frame_bits += str(int(bit)) # put the bit into the array
  count += 1
  # once we out of the inner loop, print the frame
  # print(frame_compress(frame_bits))
  full_output += frame_bits
  # print("Done!")
#print("even more done!")
xor_comp(full_output)
#with open("Output.txt", "w") as text_file:
#    print(full_output, file=text_file)
"""
color_comp()