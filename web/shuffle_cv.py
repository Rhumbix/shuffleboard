import numpy as np
import cv2
import sys

def mask_for_blue(image):
    img = cv2.imread(image)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imwrite('static/img/blue.jpg',mask)

def mask_for_red(image):
    img = cv2.imread(image)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([165,50,50])
    upper_red = np.array([185,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imwrite('static/img/red.jpg',mask)

def find_pucks(mask_file):
    img = cv2.imread(mask_file,0)
    img2 = img.copy()
    template = cv2.imread('circle_tmpl.png',0)
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
    while True:
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
    
        fill(img2, top_left, bottom_right)
        print [top_left, bottom_right]
    
        result += [[top_left[0] + w/2, top_left[1] + h/2]]

if __name__ == "__main__":
    mask_for_blue(sys.argv[1])
    mask_for_red(sys.argv[1])
    print find_pucks('static/img/blue.jpg')
