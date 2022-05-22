import mss
import numpy as np
import win32gui
import cv2 as cv

class WindowCapture:
    left = 0
    top = 0
    w = 0 # window width
    h = 0 # window height

    hwnd = None 
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name=None):
        # if no window name is given, capture entire screen
        if window_name is None:
            self.hwnd = wind32gui.GetDesktopWindow()
        else:
            # find the handle for the window we want to capture
            self.hwnd = win32gui.FindWindow(None, window_name)
            # check that the window does exist
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        # get window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 31
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        stc = mss.mss()
        scr = stc.grab({
            'left': self.left,
            'top': self.top,
            'width': self.w,
            'height': self.h
        })

        img = np.array(scr)
        img = cv.cvtColor(img, cv.IMREAD_COLOR)

        return img

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)    