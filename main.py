import cv2 as cv
import numpy as np
import os
from time import time, sleep
from window_capture import WindowCapture
from vision import Vision
import pyautogui
import random

def draw_rectangle(threshold):
    '''
    FUNCTION:
    This function takes a screenshot of the main window, then tries 
    to find your target (fishing bobber in this case) inside that screen shot.
    Finally it draws a green rectangle around that bobber and returns
    the exact position of where the bobber was found.

    PARAMETER:
    parameter is the confidence threshold of how strict we want 
    the found object to be similar to our target.
    if you put 0.99, you basically want an exact copy of your target,
    and a 0.3 means it only needs to resemble it around 30%. 
    you don't want it too low, otherwise it will recognize other 
    areas of the window as the target.
    0.67 worked for me.
    '''
    screenshot = win_to_capture.get_screenshot()
    position = vision_bobber.find(screenshot, threshold, 'rectangles')

    if position != None: # if target is located inside screenshot
        # draw green rectangle inside screenshot and display it
        output_image = vision_bobber.draw_rectangle(screenshot, position)
        cv.imshow('Fish_bot', screenshot)
        if cv.waitKey(1) == ord('q'): 
            cv.destroyAllWindows()
            print('done')
            quit()
    else: # if target isn't located, display the normal screenshot
        cv.imshow('Fish_bot', screenshot)
        if cv.waitKey(1) == ord('q'): 
            cv.destroyAllWindows()
            print('done')
            quit()
    return position
        
def cast_rod(key_to_press):
    pyautogui.press(key_to_press)            

def fish_caught(position):
    '''
    When fish is caught, the bobber dips. 
    When bobber dips, we don't recognize it anymore.
    And when we don't recognize it, a None is returned instead. 
    So we simply check for that None.
    '''
    return True if position == None else False

def reel_in_fish(last_pos):
    try:
        pyautogui.moveTo((last_pos[0] - 8), (last_pos[1] + 30), duration=random.uniform(0.1, 0.3), tween=pyautogui.easeInOutQuad)
        pyautogui.click(button= "right")
    except:
        pass

win_to_capture = WindowCapture('World of Warcraft')
vision_bobber = Vision('bobber.png')

last_pos = 0
while(True):
    cast_rod('1') # '1' here indicates the button to be pressed to cast the rod
    print('casted rod')

    sleep((0.2)) # wait a bit for bobber to be in place 
    print('waiting for fish...')

    while(True): # wait until we catch fish
        # draw rectangle around target and return position of target.
        position = draw_rectangle(0.70)
        if fish_caught(position):
            print('fish caught!!')
            break
        last_pos = position

    reel_in_fish(last_pos)
    print('taking short rest.. \n')

    # sleep for a bit to let old bobber disappear.
    # with some randomness to show some human like behavior
    sleep(random.uniform(3, 4.5)) 

    # print('FPS {}'.format(1 / (time() - loop_time)))
    # loop_time = time()