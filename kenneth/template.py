import cv2
import sys
import numpy as np

img = cv2.imread(sys.argv[1],0)
img2 = img.copy()
template = cv2.imread(sys.argv[2],0)
w, h = template.shape[::-1]

def fill(res, top_left, bottom_right):
    for i in range(top_left[1], bottom_right[1]):
        for j in range(top_left[0], bottom_right[0]):
            res[i][j] = 0

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

threshold = 0.95

method = cv2.TM_SQDIFF_NORMED

result = []
#for meth in methods:
while true:
    res = cv2.matchTemplate(img2,template,method)
#    method = eval(meth)
    
    # Apply template Matching
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if min_val > threshold:
        return result

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    result += [top_left, bottom_right]
    fill(img2, top_left, bottom_right)
    
