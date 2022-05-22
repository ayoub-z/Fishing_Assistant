import cv2 as cv
import numpy as np
import pyautogui
from window_capture import WindowCapture

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

    def display_image(self, max_val, max_loc, threshold, cropped_image, fish_bot, size_percentage=100):
        '''
        This function is purely for debugging purposes.
        A smaller window pops up, displaying what the bot can see.
        If the bobber is detected, a green triangle is drawn around it
        and this is displayed inside the smaller window.'''
        if max_val >= threshold: # if the fishing bobber is detected
            x, y = max_loc 

            # Determine the center position            
            center_x = x + int(self.bobber_w/2)
            center_y = y + int(self.bobber_h/2)

            output_image = self.draw_rectangle(cropped_image, (center_x, center_y)) # draw triangle around the bobber
            if size_percentage != 100: # if we want to resize the displayed image
                output_image = self.resize_image(output_image, size_percentage) # resize it
            cv.imshow('Fish_bot', output_image) # display the result
            cv.setWindowProperty('Fish_bot', cv.WND_PROP_TOPMOST, 1)
            if cv.waitKey(1) == ord('q'): 
                cv.destroyAllWindows()
                fish_bot.fishing = False
                print('done')
                quit()
        else: # if no bobber is detected
            if size_percentage != 100:
                cropped_image = self.resize_image(cropped_image, size_percentage)
            cv.imshow('Fish_bot', cropped_image) # display the normal image
            cv.setWindowProperty('Fish_bot', cv.WND_PROP_TOPMOST, 1)
            if cv.waitKey(1) == ord('q'): 
                cv.destroyAllWindows()
                fish_bot.fishing = False
                print('done')
                quit()

    def find(self, size_percentage, fish_bot, threshold=0.5, debug_mode=False, find_enemy=False):
        win_to_capture = WindowCapture('World of Warcraft')
        w = win_to_capture.w # window height
        h = win_to_capture.h # window width
        screenshot = win_to_capture.get_screenshot()

        # we want the middle square of the window, not the full window. since that's where the fishing bobber will be
        # and since it's better for performance to not analyse the entire window.   
        # The middle box area starts after around a 6th of the window's height, all the way down to the middle of the window. 
        # the width starts after around a 6th of the window's width and is all the way till 5/6th of the entire width

        #                        startpoint h : endpoint h,   startpoint w : endpoint w
        cropped_image = screenshot[int(h / 6) : int(h - h / 2), int(w / 6) : int(w - w / 6)]

        # The cropped image would be the square box of the full window, as shown below
        #  ________________________________
        # |     ______________________     |
        # |    |      Quare box       |    |
        # |    |______________________|    |
        # |                                |
        # |          Full window           |
        # |________________________________|

        if find_enemy:
            cropped_image = screenshot[int(h / 2 + h / 6.5) : int(h / 2 + h / 5), int(w / 4 + w / 3.25) : int((w / 1.45))]        

        result = cv.matchTemplate(cropped_image, self.bobber_img, self.method)

        # get the best match position
        _, max_val, _, max_loc = cv.minMaxLoc(result)
        if debug_mode:
            self.display_image(max_val, max_loc, threshold, cropped_image, fish_bot, size_percentage)

        # if confidence of how likely we've detected bobber, is higher than the threshold
        # it means we've found the bobber!
        if max_val >= threshold: 
            x, y = max_loc # x,y coordinates of where bobber is found

            # Determine the center position.
            # add half of the bobber's width/height, to get the very center position.
            # we also add a 6th of the window's width/height to get the actual position inside the window
            center_x = x + int(self.bobber_w/2) + (w/6) 
            center_y = y + int(self.bobber_h/2) + (h/6)
            return ((center_x, center_y), max_val, cropped_image)

    def find_enemy(self, size_percentage, fish_bot, threshold=0.5, debug_mode=False, find_enemy=True):
        find_enemy = self.find(size_percentage, fish_bot, threshold, debug_mode, find_enemy)
        if find_enemy != None:
            cv.destroyAllWindows()
            print("ENEMY SPOTTED")
            fish_bot.fishing = False
            fish_bot.emergency_escape()
            quit()

    def draw_rectangle(self, haystack_img, rectangle):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        top_left = (rectangle[0] - int(self.bobber_w/2), rectangle[1] - int(self.bobber_h/2))
        bottom_right = (top_left[0] + self.bobber_w, top_left[1] + self.bobber_h)

        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                    lineType=line_type, thickness=2)
        return haystack_img

    def resize_image(self, image, size_percentage):
        # size_percentage is percent of original size

        width = int(image.shape[1] * size_percentage / 100)
        height = int(image.shape[0] * size_percentage / 100)
        dim = (width, height)

        # resize image
        image = cv.resize(image, dim, interpolation = cv.INTER_AREA)
        return image