#DocJade

# Functions that compress.

import cv2
import numpy as np

#TODO rewrite these functions to be more generic.


#TODO update functions to use arrays of colors instead of strings.


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

def image_to_change_array(frame1: [int], frame2: [int]):
   # check that arrays are same length for sanity
   if len(frame1) != len(frame2):
      # Frames are not the same length!
      raise "image_to_change_array: Frames are not the same size!"

   # Now we shall compare each color, and add them to a new array that stores the changes.
   # no change is stored as -1
   changes = list(int)

   for i in len(frame1):
      if frame1[i] == frame2[i]:
         # colors are the same, no change.
         changes.append(-1)
      else:
         # Colors are different, store the new color.
         changes.append(frame2[i])
   
   # return the changes array.
   return changes


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

def quadtree_compression(frame: [int]):
   #TODO!
   #https://en.wikipedia.org/wiki/Quadtree
   return "#TODO!"

def change_compression(frame1: [int], frame2: [int]):
   # frame 1 is the previous frame.

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

   changes = image_to_change_array(frame1,frame2)

   # Now that all the differences are stored, we can build the output string.

   changeless_count = 0
   output_string = ""

   for i in len(changes):
      # check for a -1
      if changes[i] == -1:
         # no change, increment.
         changeless_count += 1
         continue
      else:
         # Change!
         # append the change amount to the string
         output_string += str(changeless_count)
         # reset the count
         changeless_count = 0
         # Add the separator
         output_string += ":"
         # Then append the new color.
         output_string += changes[i]
         continue

   # now we've worked through the whole frame, cap it and ship it!
   output_string += ">"

   return output_string