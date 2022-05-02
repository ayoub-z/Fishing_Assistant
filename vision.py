import cv2 as cv
import numpy as np
import pyautogui

class Vision:

    # properties
    bobber_img = None
    bobber_w = 0
    bobber_h = 0
    method = None

    def __init__(self, bobber_img_path, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.bobber_img = cv.imread(bobber_img_path, cv.IMREAD_UNCHANGED)
        self.bobber_img = self.bobber_img[...,:3]

        # Save the dimensions of the bobber image
        self.bobber_w = self.bobber_img.shape[1]
        self.bobber_h = self.bobber_img.shape[0]

        # 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.5, debug_mode=None):
        result = cv.matchTemplate(haystack_img, self.bobber_img, self.method)

        # get the best match position
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # print("Confidence: ", round(max_val, 2))
        if max_val >= threshold:
            
            marker_color = (255,0, 255)
            marker_type = cv.MARKER_CROSS
            
            x, y = max_loc

            # marker_color = (255, 0, 255)
            # marker_type = cv.MARKER_CROSS

            # Determine the center position
            center_x = x + int(self.bobber_w/2)
            center_y = y + int(self.bobber_h/2)
            return ((center_x, center_y), max_val)

    def draw_rectangle(self, haystack_img, rectangle):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        top_left = (rectangle[0] - int(self.bobber_w/2), rectangle[1] - int(self.bobber_h/2))
        bottom_right = (top_left[0] + self.bobber_w, top_left[1] + self.bobber_h)

        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                    lineType=line_type, thickness=2)
        return haystack_img
        
        
    #     elif debug_mode == 'points':
    #         # Draw the center point
    #         cv.drawMarker(haystack_img, (center_x, center_y), 
    #                     color=marker_color, markerType=marker_type, 
    #                     markerSize=40, thickness=2)

    #     if debug_mode:
    #         cv.imshow('Matches', haystack_img)
    #         #cv.waitKey()
    #         #cv.imwrite('result_click_point.jpg', haystack_img)